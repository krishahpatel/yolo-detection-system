from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data="data/splits/data.yaml",
    epochs=30,
    imgsz=640,
    batch=8,
    name="workspace_v1"
)