<p align="center">
  <img width="40%" src="docs/result.jpg">
</p>

## MTG-Card-Segmentation-YOLO11

## **Overview:**  
This project provides a simple end-to-end pipeline for training a custom [YOLO11](https://github.com/ultralytics/ultralytics) model that segments high-resolution Magic: The Gathering card scans to detect 7 card face elements—**card_title**, **card_art**, **card_type**, **card_set_symbol**, **card_mana_cost**, **card_oracle_text**, and **card_power_toughness**—so that it can accurately locate these segments in new, unseen card images.

## Workflow

1. **Data Download & Extraction**  
   - **Script:** `unzip-dataset.py`  
     Downloads the raw ZIP files (images, training annotations, and validation annotations) if they don’t already exist, then extracts the contents from their subfolders (or directly from the root for the images ZIP) into designated directories.

2. **Annotation Conversion & Data Splitting**  
   - **Script:** `convert-dataset.py`  
     Converts XML annotation files into YOLO-format labels. The script processes training annotations (from `data/annotations`) and validation annotations (from `data/control_annotations`) separately, copying the corresponding images into `data/images/train` and `data/images/val` while saving the labels in `data/labels/train` and `data/labels/val`.

3. **Dataset Configuration**  
   - **Script:** `setup-yolo11-yaml.py`  
     Generates the YAML configuration file (`my_custom_dataset.yaml`) for YOLO11. This file specifies the relative paths to the training (`images/train`) and validation (`images/val`) image directories, the number of classes (`nc: 7`), and the class names.

4. **Model Training**  
   - **Script:** `train-yolo.py`  
     Loads a pretrained YOLO11 model and fine-tunes it on your custom dataset as defined in the YAML file. Training parameters such as epochs and image size are configured within the script.

5. **Inference**  
   - **Script:** `detect_image.py`  
     Loads the trained model and performs inference on a new, unannotated card image. The script displays the image with bounding boxes around detected card elements and saves the output image for review.

---

## Environment Setup

1. **Create a Virtual Environment** (Python 3.9+ recommended):

   ```bash
   python -m venv venv
   # Activate on Windows:
   venv\Scripts\activate
   # or on Linux/MacOS:
   source venv/bin/activate
   ```

2. **Install Required Packages:**

   ```bash
   pip install -r requirements.txt
   ```

---

## How to Use

1. **Download & Extract Dataset:**
   ```bash
   python unzip-dataset.py
   ```

2. **Convert Annotations & Split Data:**
   ```bash
   python convert-dataset.py
   ```

3. **Generate YAML Configuration:**
   ```bash
   python setup-yolo11-yaml.py
   ```

4. **Train the Model:**
   ```bash
   python train-yolo.py
   ```

5. **Run Inference on a New Image:**
   ```bash
   python detect_image.py path/to/your/image.jpg
   ```

---

## Resources

- **Dataset (HuggingFace):**  
  [MTG Face Objects Classification Dataset](https://huggingface.co/datasets/JakeTurner616/mtg_face_objects_classifcation)

- **Pre-trained Model (HuggingFace):**  
  [MTG Card Segmentation YOLO11 Model](https://huggingface.co/JakeTurner616/mtg-card-segmentation-yolo11)

---

## Results


<div align="center">
  <img src="docs/results.png" alt="Training Metrics Graph" />
</div><br>


| Epoch | Time (s) | Train Box Loss | Train Cls Loss | Train DFL Loss | Precision (B) | Recall (B) | mAP50 (B) | mAP50-95 (B) | Val Box Loss | Val Cls Loss | Val DFL Loss | LR PG0  | LR PG1  | LR PG2  |
|-------|---------|---------------|---------------|---------------|--------------|------------|-----------|-------------|--------------|--------------|--------------|---------|---------|---------|
| 1     | 27.19   | 1.506         | 3.816         | 1.438         | 0.033        | 0.251      | 0.095     | 0.048       | 1.069        | 3.907        | 1.296        | 4.55e-05 | 4.55e-05 | 4.55e-05 |
| 10    | 271.27  | 0.861         | 1.216         | 1.007         | 0.980        | 0.270      | 0.718     | 0.590       | 0.818        | 2.804        | 0.908        | 4.89e-04 | 4.89e-04 | 4.89e-04 |
| 25    | 700.46  | 0.741         | 0.668         | 0.940         | 0.955        | 0.977      | 0.975     | 0.793       | 0.644        | 0.814        | 0.898        | 6.93e-04 | 6.93e-04 | 6.93e-04 |
| 50    | 1395.36 | 0.664         | 0.530         | 0.916         | 0.970        | 0.975      | 0.970     | 0.790       | 0.699        | 0.607        | 0.891        | 4.68e-04 | 4.68e-04 | 4.68e-04 |
| 75    | 2033.89 | 0.621         | 0.477         | 0.900         | 0.957        | 0.973      | 0.968     | 0.802       | 0.657        | 0.561        | 0.879        | 2.43e-04 | 2.43e-04 | 2.43e-04 |
| 90    | 2407.26 | 0.575         | 0.439         | 0.891         | 0.970        | 0.974      | 0.973     | 0.804       | 0.647        | 0.530        | 0.874        | 1.08e-04 | 1.08e-04 | 1.08e-04 |
| 100   | 2649.53 | 0.573         | 0.530         | 0.904         | 0.961        | 0.973      | 0.965     | 0.798       | 0.627        | 0.567        | 0.867        | 1.81e-05 | 1.81e-05 | 1.81e-05 |


## License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for more details.
