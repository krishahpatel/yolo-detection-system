# src/detect.py

from ultralytics import YOLO
import cv2
import yaml
import time

from logger import DetectionLogger


class Detector:

    def __init__(self, config_path="config/config.yaml"):

        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.model = None
        self.class_names = None

        self.prev_time = time.time()

        # Per-class thresholds
        self.class_thresholds = {
            "cup": 0.60,
            "laptop": 0.70,
            "notebook": 0.60,
            "person": 0.35,
            "phone": 0.70
        }

        self.logger = DetectionLogger(
            self.config["logging"]["database_path"]
        )

    def load_model(self):

        model_path = self.config["model"]["weights_path"]

        print(f"[INFO] Loading model: {model_path}")

        self.model = YOLO(model_path)
        self.class_names = self.model.names

        print("[INFO] Model loaded successfully")

    def detect_frame(self, frame):

        results = self.model.predict(
            frame,
            conf=self.config["model"]["confidence_threshold"],
            iou=self.config["model"]["nms_threshold"],
            imgsz=self.config["model"]["image_size"],
            verbose=False
        )

        detections = []

        for box in results[0].boxes:

            cls_id = int(box.cls[0])
            conf = float(box.conf[0])

            class_name = self.class_names[cls_id]

            required_conf = self.class_thresholds.get(class_name, 0.5)

            if conf < required_conf:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            width = x2 - x1
            height = y2 - y1

            detections.append({
                "class_id": cls_id,
                "class_name": class_name,
                "confidence": conf,
                "bbox": [x1, y1, x2, y2],
                "width": width,
                "height": height
            })

        return detections

    def draw_results(self, frame, detections):

        output = frame.copy()

        for det in detections:

            x1, y1, x2, y2 = det["bbox"]

            label = f"{det['class_name']} {det['confidence']:.2f}"

            cv2.rectangle(
                output,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                output,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        fps = self.get_fps()

        cv2.putText(
            output,
            f"FPS: {fps:.1f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        return output

    def get_fps(self):

        current_time = time.time()
        diff = current_time - self.prev_time

        fps = 1 / diff if diff > 0 else 0

        self.prev_time = current_time

        return fps

    def close(self):
        self.logger.close()


def main():

    detector = Detector()
    detector.load_model()

    cap = cv2.VideoCapture(detector.config["camera"]["source"])

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, detector.config["camera"]["width"])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, detector.config["camera"]["height"])

    if not cap.isOpened():
        print("[ERROR] Could not open webcam")
        return

    print("[INFO] Webcam started")
    print("[INFO] Press 'q' to quit")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        detections = detector.detect_frame(frame)

        # Log detections
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]

            detector.logger.log_detection(
                det["class_name"],
                det["confidence"],
                (x1, y1, x2 - x1, y2 - y1)
            )

        output_frame = detector.draw_results(frame, detections)

        cv2.imshow("Workspace Monitoring System", output_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    detector.close()
    cv2.destroyAllWindows()

    print("[INFO] Application closed")


if __name__ == "__main__":
    main()
