# Issue Reporting Model

This directory contains the necessary code and structure for fine-tuning an image classification model to categorize municipal issues reported by citizens. The model identifies problems like potholes, water leaks, waste, etc., from uploaded images.

## Model Used

We utilize a **pre-trained ResNet-50** model from `torchvision.models`. ResNet-50 is a powerful Convolutional Neural Network (CNN) architecture initially trained on the vast ImageNet dataset. This allows us to leverage its extensive knowledge of image features and apply it to our specific task through **transfer learning**.

### Why ResNet-50 and Transfer Learning?

*   **Efficiency**: Training a deep learning model from scratch is computationally expensive and requires a massive dataset. ResNet-50, being pre-trained, already possesses a strong ability to recognize various visual patterns.
*   **Effectiveness**: By fine-tuning a pre-trained model, we adapt its learned features to our specific problem categories with a comparatively smaller dataset, leading to faster training and better performance.

## How the Model Works (Inference)

Once the model is trained, here's how it processes a new input image to identify a problem:

1.  **Image Preprocessing**:
    *   The input image is resized to 224x224 pixels and converted into a PyTorch tensor.
    *   It is then normalized using the mean and standard deviation from the ImageNet dataset, which the original ResNet-50 was trained on. This standardization ensures the image data is in the format expected by the model.

2.  **Feature Extraction**:
    *   The preprocessed image is fed through the convolutional layers of the ResNet-50 model. These layers act as sophisticated feature extractors, identifying hierarchical visual characteristics within the image, such as edges, textures, and object parts.

3.  **Classification**:
    *   The extracted features are then passed to a newly added fully connected layer (the classification head).
    *   This layer, specifically fine-tuned on our dataset, outputs a probability score for each of the predefined categories (e.g., Roads, Water, Electricity, Waste, Safety, Other).

4.  **Prediction**:
    *   The category with the highest probability score is selected as the model's prediction, indicating the type of municipal problem identified in the image.

## Requirements

To set up and run this model, you'll need the following Python libraries. It's recommended to install them within a virtual environment.

To install the dependencies, navigate to the `model` directory and run:

```bash
pip install -r requirements.txt
```

Alternatively, the core dependencies are:

*   `torch`
*   `torchvision`
*   `pandas`
*   `Pillow`

## Data Preparation

Before training or using the model, prepare your data as follows:

### `model/dataset` folder:

*   **Images**: Place all your raw problem images (for potential future use or inference examples) in `model/dataset/images/`. (You might need to create this `images` subdirectory).
*   **CSV file (`dataset.csv`)**: Create a CSV file at `model/dataset/dataset.csv` with two columns:
    *   `image_name`: The filename of the image (e.g., `pothole1.jpg`).
    *   `category`: The corresponding problem category (e.g., `Roads`, `Water`, `Electricity`, `Waste`, `Safety`, `Other`).

### `model/training` folder:

*   **Images**: Create an `images` subdirectory at `model/training/images/` and place your training images there.
*   **CSV file (`train.csv`)**: Create a CSV file at `model/training/train.csv` with the same two-column format as `dataset.csv`. This file maps training image filenames to their respective categories.

## Running the Model

Once your data is prepared and dependencies are installed, you can run the `model.py` script from the project root:

```bash
python model/model.py
```

This will initiate the training process and, upon completion, save the trained model weights to `model/issue_reporting_model.pth` and then export the model to ONNX format in the `model/onnx/` directory.

## Data Generation (Optional)

If you don't have a real dataset, you can generate dummy images and corresponding CSV files for both the `dataset` and `training` folders using the `generate_data.py` script. This script will create placeholder images with category labels and populate the `dataset.csv` and `train.csv` files.

To generate data, run the following command from the project root:

```bash
python model/generate_data.py
```

This will create:
- `model/dataset/images/` with dummy images and `model/dataset/dataset.csv`
- `model/training/images/` with dummy images and `model/training/train.csv`

## Running the Model (Training and Fine-tuning)

To train the model initially and then fine-tune it on each individual image in the training set, run the `model.py` script from the project root:

```bash
python model/model.py
```

This script will first perform a standard training loop over multiple epochs. After this initial training, it will then iterate through each image in the `model/training/images/` folder and perform a fine-tuning step on that single image. Upon completion, it will save the trained model weights to `model/issue_reporting_model.pth` and then export the model to ONNX format in the `model/onnx/` directory.

## Running the FastAPI Server

After training the model and ensuring `model/issue_reporting_model.pth` exists, you can start the FastAPI server to expose the model for inference. From the project root, run:

```bash
uvicorn model.api:app --reload
```

This will start the server, typically at `http://127.0.0.1:8000`. You can then access the interactive API documentation at `http://127.0.0.1:8000/docs` to test the `/predict` endpoint.
