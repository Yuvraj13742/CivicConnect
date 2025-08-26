import torch
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import os
from torchvision import models
import torch.nn as nn
import torch.optim as optim

def get_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    else:
        return torch.device("cpu")

device = get_device()
print(f"Using device: {device}")

# Define categories - these should be loaded from the CSV or configured
CATEGORIES = ['Roads', 'Water', 'Electricity', 'Waste', 'Safety', 'Other']
NUM_CLASSES = len(CATEGORIES)

class IssueDataset(Dataset):
    def __init__(self, csv_file, root_dir, transform=None):
        self.annotations = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, idx):
        img_name = os.path.join(self.root_dir, self.annotations.iloc[idx, 0])
        image = Image.open(img_name).convert('RGB')
        label = self.annotations.iloc[idx, 1] # Assuming the second column is the label

        # Convert label to one-hot encoding or class index
        label_idx = CATEGORIES.index(label) # This needs error handling if label not found

        if self.transform:
            image = self.transform(image)

        return image, label_idx

# Image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Load a pre-trained ResNet model
model = models.resnet50(pretrained=True)

# Replace the last fully connected layer to match the number of categories
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, NUM_CLASSES)

model = model.to(device)

# Placeholder for dataset and dataloader creation
train_dataset = IssueDataset(csv_file='model/training/train.csv', root_dir='model/training/images', transform=transform)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

def fine_tune_on_single_image(model, image, label, criterion, optimizer):
    model.train() # Ensure model is in training mode
    image, label = image.to(device), label.to(device)

    optimizer.zero_grad()
    outputs = model(image)
    loss = criterion(outputs, label)
    loss.backward()
    optimizer.step()
    return loss.item()

def train_model(model, train_loader, criterion, optimizer, num_epochs=10):
    model.train()
    for epoch in range(num_epochs):
        running_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"Epoch {epoch+1}, Loss: {running_loss/len(train_loader)}")

if __name__ == '__main__':
    print("Starting initial training...")
    train_model(model, train_loader, criterion, optimizer, num_epochs=5) # Reduced epochs for example

    # After initial training, fine-tune on each image from the training set individually
    print("Starting fine-tuning on individual images...")
    single_image_loader = DataLoader(train_dataset, batch_size=1, shuffle=False) # Use batch size 1 for individual fine-tuning
    for i, (images, labels) in enumerate(single_image_loader):
        loss = fine_tune_on_single_image(model, images, labels, criterion, optimizer)
        if (i+1) % 100 == 0: # Print loss every 100 images
            print(f"Fine-tuning image {i+1}, Loss: {loss}")

    # Save the trained model's state_dict
    model_save_path = "model/issue_reporting_model.pth"
    torch.save(model.state_dict(), model_save_path)
    print(f"Trained model saved to {model_save_path}")

    # ONNX export
    dummy_input = torch.randn(1, 3, 224, 224).to(device) # Batch size, channels, height, width
    onnx_path = "model/onnx/issue_reporting_model.onnx"
    torch.onnx.export(model, dummy_input, onnx_path, verbose=True, input_names=["input"], output_names=["output"])
    print(f"Model exported to ONNX at {onnx_path}")
