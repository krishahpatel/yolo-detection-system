from ultralytics import YOLO
import cv2
import time
import os

# Load trained model
model = YOLO("models/weights/best_v1_map853.pt")

# Create assets folder if it does not exist
os.makedirs("assets", exist_ok=True)

# Start webcam
cap = cv2.VideoCapture(0)

print("Press Q to quit")
print("Press S to save screenshot")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to access webcam")
        break

    # Run inference
    results = model(frame, verbose=False, conf=0.6)

    # Draw detections
    annotated = results[0].plot()

    # Show window
    cv2.imshow("Workspace v1 - Real World Test", annotated)

    key = cv2.waitKey(1) & 0xFF

    # Save screenshot
    if key == ord('s'):
        filename = f"assets/detection_sample_{int(time.time())}.jpg"
        cv2.imwrite(filename, annotated)
        print(f"Screenshot saved: {filename}")

    # Quit
    if key == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()