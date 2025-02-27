# 3rd script to run: setup-yolo11-yaml.py
import os
import subprocess

# Step 1: Install YOLO11 (Ultralytics) if not already installed
try:
    import ultralytics
    print("Ultralytics (YOLO11) already installed.")
except ImportError:
    print("Installing ultralytics...")
    subprocess.check_call(["pip", "install", "ultralytics"])

# Step 2: Define absolute paths for your train and validation image directories.
# Adjust these if your folders are elsewhere.
train_path = os.path.abspath(os.path.join("data", "images", "train"))
val_path   = os.path.abspath(os.path.join("data", "images", "val"))

# Updated YAML content with 7 classes
yaml_content = f"""
train: {train_path}
val: {val_path}
nc: 7
names:
  - card_title
  - card_art
  - card_type
  - card_set_symbol
  - card_mana_cost
  - card_oracle_text
  - card_power_toughness
"""

# Step 3: Write the YAML file. Place it in your project root.
yaml_filename = "my_custom_dataset.yaml"
yaml_filepath = os.path.join(os.getcwd(), yaml_filename)

with open(yaml_filepath, "w") as f:
    f.write(yaml_content.strip())

print(f"Dataset YAML file created successfully at: {yaml_filepath}")
