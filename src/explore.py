from ultralytics import YOLO
import cv2
import os

# Build path relative to this file's location
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img_path = os.path.join(base_dir, "assets", "image.png")

# Load model and image
model = YOLO("yolov8n.pt")
img = cv2.imread(img_path)

if img is None:
    print(f"ERROR: Could not load image at {img_path}")
    print("Make sure test_image.jpg exists in your assets/ folder")
    exit()

# Run inference
results = model(img)
result = results[0]

# Print raw outputs
print("\n--- Bounding Boxes (x1, y1, x2, y2) ---")
print(result.boxes.xyxy)

print("\n--- Confidence Scores ---")
print(result.boxes.conf)

print("\n--- Class IDs ---")
print(result.boxes.cls)

print("\n--- Class Names Dictionary ---")
print(result.names)

# Print in a human-readable format
print("\n--- Human Readable Summary ---")
for i, box in enumerate(result.boxes):
    class_id = int(box.cls[0])
    class_name = result.names[class_id]
    confidence = float(box.conf[0])
    x1, y1, x2, y2 = box.xyxy[0].tolist()
    print(f"Object {i+1}: {class_name} | Confidence: {confidence:.2f} | Box: ({int(x1)}, {int(y1)}) to ({int(x2)}, {int(y2)})")