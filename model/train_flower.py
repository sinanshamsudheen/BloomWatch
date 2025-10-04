# train_flowers.py
from ultralytics import YOLO

# --- 1. Load a pre-trained YOLOv8 model ---
# We use 'yolov8n.pt' (n for nano), which is the smallest and fastest.
# You can also use 'yolov8s.pt' for a balance of speed and accuracy.
model = YOLO('yolov8n.pt')

# --- 2. Define the path to your dataset's YAML file ---
# !!! IMPORTANT !!!
# You MUST replace this path with the actual path to the 'data.yaml' file
# from the dataset you downloaded from Roboflow.
yaml_path = 'data.yaml'

# --- 3. Train the model ---
# The train function handles all data loading and augmentation automatically.
try:
    results = model.train(
        data=yaml_path,   # Path to your data.yaml file
        epochs=100,       # Number of training epochs (100 is a good start)
        imgsz=640,        # Image size for training (640x640)
        batch=8,          # Batch size (you can lower this to 4 or 2 if you run out of GPU memory)
        name='yolov8_flower_model_final' # Name for the results folder
    )
    print("✅ Training completed successfully!")
    print("Your trained model is saved in the 'runs/detect/yolov8_flower_model_final/weights/' directory as 'best.pt'.")

except Exception as e:
    print(f"❌ An error occurred during training: {e}")