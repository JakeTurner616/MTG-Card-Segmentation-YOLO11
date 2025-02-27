# 4th script to run: train-yolo.py
from ultralytics import YOLO

# Load a pretrained YOLO11 model (using the YOLO11n variant here, adjust if needed)
model = YOLO("yolo11n.pt")

# Start training on your custom dataset defined in the YAML file.
results = model.train(data="data/my_custom_dataset.yaml", epochs=100, imgsz=640)

print("Training complete!")
