# 1st script to run: unzip-dataset.py

# Download the dataset and annotations ZIP files and unzip them.
import os
import zipfile
import shutil
import requests

def download_file(url, filename):
    """Download a file from the given URL and save it as filename."""
    print(f"Downloading {filename}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an error for bad status codes
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"Downloaded {filename} successfully.")

# Download ZIP files if they don't exist locally

# Use the new dataset ZIP from Hugging Face (images are at the root of the ZIP)
if not os.path.exists("dataset.zip"):
    download_file("https://huggingface.co/datasets/JakeTurner616/mtg_face_objects_classifcation/resolve/main/images/high-res-card-scan-images.zip?download=true", "dataset.zip")
else:
    print("dataset.zip already exists.")

# Annotations and control annotations come from my server for simplicity although the can be found on the HF dataset page
if not os.path.exists("annotations.zip"):
    download_file("https://files.serverboi.org/api/files/cat?path=%2Fannotations.zip&share=DjI1xGk", "annotations.zip")
else:
    print("annotations.zip already exists.")

if not os.path.exists("Control_annotations.zip"):
    download_file("https://files.serverboi.org/api/files/cat?path=%2FControl+annotations.zip&share=XWpibn7", "Control_annotations.zip")
else:
    print("Control_annotations.zip already exists.")

def unzip_and_move(zip_path, subfolder, dest_dir):
    """
    Extracts the given ZIP file into a temporary directory,
    then moves files from the specified subfolder (if provided) to dest_dir.
    If subfolder is an empty string, files are moved directly from the root.
    """
    temp_dir = os.path.join(dest_dir, "temp_extract")
    os.makedirs(temp_dir, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    # If a subfolder is specified, use it; otherwise, use the root of the extracted contents.
    src_dir = os.path.join(temp_dir, subfolder) if subfolder else temp_dir
    
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)
            shutil.move(src_file, dest_file)
    
    shutil.rmtree(temp_dir)
    print(f"Extracted {zip_path} {'from subfolder ' + subfolder if subfolder else ''} to {dest_dir}")

# Set target directories and ensure they exist
images_dir = os.path.join("data", "images")
annotations_dir = os.path.join("data", "annotations")
control_annotations_dir = os.path.join("data", "control_annotations")

os.makedirs(images_dir, exist_ok=True)
os.makedirs(annotations_dir, exist_ok=True)
os.makedirs(control_annotations_dir, exist_ok=True)

# Unzip each archive using the appropriate subfolder names:
# For dataset.zip, no subfolder is present (files are at the root), so pass an empty string.
unzip_and_move("dataset.zip", "", images_dir)

# For annotations.zip, files are under a subfolder named "annotations"
unzip_and_move("annotations.zip", "annotations", annotations_dir)

# For Control_annotations.zip, files are under a subfolder named "Control annotations"
unzip_and_move("Control_annotations.zip", "Control annotations", control_annotations_dir)
