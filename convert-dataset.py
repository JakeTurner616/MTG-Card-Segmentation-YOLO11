# 2nd code script to run: convert-dataset.py
# Convert the dataset annotations from labellmg .xml to YOLO format and split the dataset into training and validation sets.

import os
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image
import shutil

# Expanded mapping from XML class names to numeric class IDs
CLASS_MAPPING = {
    'card_title': 0,
    'card_art': 1,
    'card_type': 2,
    'card_set_symbol': 3,
    'card_mana_cost': 4,
    'card_oracle_text': 5,
    'card_power_toughness': 6   # New class added
}

# Directories
annotations_dir = 'data/annotations'            # Training annotations
control_annotations_dir = 'data/control_annotations'  # Validation annotations
images_root = os.path.join("data", "images")      # All images (from dataset.zip)
labels_root = os.path.join("data", "labels")

# Create subdirectories for train and validation images and labels
train_images_dir = os.path.join(images_root, "train")
val_images_dir = os.path.join(images_root, "val")
train_labels_dir = os.path.join(labels_root, "train")
val_labels_dir = os.path.join(labels_root, "val")

for d in [train_images_dir, val_images_dir, train_labels_dir, val_labels_dir]:
    os.makedirs(d, exist_ok=True)

def process_annotation(xml_file, image_dest_dir, label_dest_dir):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Extract the image filename from the XML and use its basename
    xml_filename = root.find('filename').text
    image_filename = os.path.basename(xml_filename)
    
    # Source image location (all images initially reside in images_root)
    src_image_path = os.path.join(images_root, image_filename)
    # Destination image location (train or val folder)
    dest_image_path = os.path.join(image_dest_dir, image_filename)
    
    # Copy image to destination folder if not already there
    if not os.path.exists(dest_image_path):
        shutil.copy(src_image_path, dest_image_path)
    
    # Open the copied image to obtain its dimensions
    im = Image.open(dest_image_path)
    w, h = im.size

    yolo_lines = []
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in CLASS_MAPPING:
            continue  # Skip unknown classes
        cls_id = CLASS_MAPPING[cls]
        
        bndbox = obj.find('bndbox')
        xmin = float(bndbox.find('xmin').text)
        ymin = float(bndbox.find('ymin').text)
        xmax = float(bndbox.find('xmax').text)
        ymax = float(bndbox.find('ymax').text)
        
        # Convert bounding box to YOLO format: normalized center x, center y, width, height
        x_center = ((xmin + xmax) / 2) / w
        y_center = ((ymin + ymax) / 2) / h
        bbox_width = (xmax - xmin) / w
        bbox_height = (ymax - ymin) / h
        
        yolo_lines.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}")

    # Save the label file with the same base name as the image into the label destination folder
    label_filename = os.path.splitext(image_filename)[0] + ".txt"
    label_filepath = os.path.join(label_dest_dir, label_filename)
    with open(label_filepath, 'w') as f:
        f.write("\n".join(yolo_lines))
    
    print(f"Processed {image_filename} -> {label_filepath}")

# Process training annotations (from annotations folder)
for xml_file in Path(annotations_dir).rglob("*.xml"):
    process_annotation(str(xml_file), train_images_dir, train_labels_dir)

# Process validation annotations (from control_annotations folder)
for xml_file in Path(control_annotations_dir).rglob("*.xml"):
    process_annotation(str(xml_file), val_images_dir, val_labels_dir)

print("Annotation conversion and dataset splitting complete.")