import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import random
import numpy as np

# Define categories (must match model.py)
CATEGORIES = ['Roads', 'Water', 'Electricity', 'Waste', 'Safety', 'Other']

def generate_dummy_image(output_path, category, img_size=(224, 224), text_color=(255, 255, 255)):
    image = Image.new('RGB', img_size, color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    draw = ImageDraw.Draw(image)

    # Try to load a default font or use a generic one
    try:
        # On Windows, a common font path is C:\Windows\Fonts\arial.ttf
        # On Linux/macOS, it might be /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf or similar
        font = ImageFont.truetype("arial.ttf", 20) # This might require font installation or a specific path
    except IOError:
        font = ImageFont.load_default()

    # Draw category text
    text = f"{category} Problem"
    # Get text bounding box (left, top, right, bottom)
    bbox = draw.textbbox((0, 0), text, font=font) # Calculate bounding box
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (img_size[0] - text_width) // 2
    text_y = (img_size[1] - text_height) // 2
    draw.text((text_x, text_y), text, font=font, fill=text_color)

    # Add some random shapes/lines for variety
    for _ in range(random.randint(1, 3)):
        shape_type = random.choice(['line', 'rectangle', 'ellipse'])
        x1, y1 = random.randint(0, img_size[0]), random.randint(0, img_size[1])
        x2, y2 = random.randint(0, img_size[0]), random.randint(0, img_size[1])
        fill_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        if shape_type == 'line':
            draw.line([(x1, y1), (x2, y2)], fill=fill_color, width=random.randint(1, 3))
        elif shape_type == 'rectangle':
            draw.rectangle([(min(x1, x2), min(y1, y2)), (max(x1, x2), max(y1, y2))], fill=fill_color)
        else: # ellipse
            draw.ellipse([(min(x1, x2), min(y1, y2)), (max(x1, x2), max(y1, y2))], fill=fill_color)

    image.save(output_path)

def generate_dataset(base_dir, num_images_per_category=20):
    images_dir = os.path.join(base_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)

    data = []
    for category in CATEGORIES:
        for i in range(num_images_per_category):
            img_name = f"{category.lower().replace(' ', '_')}_{i:03d}.png"
            img_path = os.path.join(images_dir, img_name)
            generate_dummy_image(img_path, category)
            data.append({'image_name': os.path.join('images', img_name), 'category': category})

    df = pd.DataFrame(data)
    csv_path = os.path.join(base_dir, 'dataset.csv' if 'dataset' in base_dir else 'train.csv')
    df.to_csv(csv_path, index=False)
    print(f"Generated {len(data)} images and {csv_path}")

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(project_root)

    # Generate data for dataset folder
    dataset_path = os.path.join(model_dir, 'dataset')
    generate_dataset(dataset_path, num_images_per_category=10) # Fewer for dataset example

    # Generate data for training folder
    training_path = os.path.join(model_dir, 'training')
    generate_dataset(training_path, num_images_per_category=50) # More for training
