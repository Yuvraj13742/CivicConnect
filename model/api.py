from fastapi import FastAPI, UploadFile, File
from PIL import Image
import io
import torch
from torchvision import transforms
from torchvision import models
import torch.nn as nn
import os

CATEGORIES = ['Roads', 'Water', 'Electricity', 'Waste', 'Safety', 'Other']
NUM_CLASSES = len(CATEGORIES)

app = FastAPI()

# Device configuration
def get_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    else:
        return torch.device("cpu")

device = get_device()

# Load the pre-trained model and adjust the final layer
model = models.resnet50(pretrained=False) # We load our own weights, so no pretrained=True here
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, NUM_CLASSES)

# Load the trained state_dict
model_path = "model/issue_reporting_model.pth"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model weights not found at {model_path}. Please train the model first by running model.py")
model.load_state_dict(torch.load(model_path, map_location=device))
model.to(device)
model.eval() # Set model to evaluation mode

# Image transformations (must be the same as used during training)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

@app.post("/predict/")
async def predict_issue(file: UploadFile = File(...)):
    # Read image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')

    # Preprocess image
    image = transform(image).unsqueeze(0).to(device) # Add batch dimension and move to device

    # Make prediction
    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs.data, 1)
        predicted_category_idx = predicted.item()

    predicted_category = CATEGORIES[predicted_category_idx]
    return {"filename": file.filename, "predicted_category": predicted_category}
