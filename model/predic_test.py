# test_model.py
from ultralytics import YOLO
from PIL import Image

# --- 1. Load Your Custom Model ---
# IMPORTANT: Replace this path with the actual path to your 'best.pt' file.
model_path = 'runs/detect/yolov8_flower_model_final/weights/best.pt'
model = YOLO(model_path)

# --- 2. Define the Image to Test ---
# Use a new image that the model has never seen before.
# You can use a local file path or a URL.
image_to_test = '/mnt/e/Projects/VSC/Bloomwatch/cactus plant - Google Search/wcactus.jpg'

# --- 3. Run the Prediction ---
results = model(image_to_test)

# --- 4. View and Save the Results ---
# The 'results' object contains all the detection information.
# The easiest way to see the output is to display or save the annotated image.
for r in results:
    # Convert the result to a PIL Image object
    im_array = r.plot()  # 'plot()' draws the bounding boxes on the image
    im = Image.fromarray(im_array[..., ::-1])  # Convert to RGB

    # Display the image
    print("Displaying detection results...")
    im.show()

    # Save the result
    output_filename = 'prediction_result.jpg'
    im.save(output_filename)
    print(f"Results saved to {output_filename}")