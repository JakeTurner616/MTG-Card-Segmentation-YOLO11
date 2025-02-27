# Final inference script to detect objects in an image using a trained YOLOv5 model.
# Usage: python detect_image.py <image_file>
import sys
import os
import cv2
from ultralytics import YOLO

def main(image_path: str, model_path: str = "runs/detect/train15/weights/best.pt", save_dir: str = "inference_results"):
    # Load the trained model (adjust model_path if needed)
    model = YOLO(model_path)
    
    # Run inference on the image; returns a list of result objects
    results = model(image_path)
    
    # Access the first (and only) result
    result = results[0]
    
    # Display the image with detection boxes
    result.show()
    
    # Get the plotted image (with boxes) as a numpy array.
    # result.plot() returns the image with predictions drawn on it.
    plotted_image = result.plot()  
    
    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)
    
    # Create an output filename based on the input image name
    output_filename = os.path.join(save_dir, "detected_" + os.path.basename(image_path))
    
    # Save the plotted image using OpenCV
    cv2.imwrite(output_filename, plotted_image)
    print(f"Result saved to {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python detect_image.py <image_file>")
        sys.exit(1)
    image_file = sys.argv[1]
    main(image_file)
