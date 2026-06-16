from ultralytics import YOLO

model = YOLO("runs/detect/new_workspace/weights/best.pt")

results = model(
    "image.png",
    conf=0.1,
    show=True
)

print(results[0].boxes)     