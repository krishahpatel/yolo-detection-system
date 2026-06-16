# src/detect.py

from ultralytics import YOLO
import cv2
import yaml
import time


class Detector:
    def __init__(self, config_path="config/config.yaml"):
        self.config_path = config_path

        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.model = None
        self.class_names = None
        self.prev_time = time.time()

    def load_model(self):
        model_path = self.config["model"]["weights_path"]

        print(f"[INFO] Loading model: {model_path}")

        self.model = YOLO(model_path)
        self.class_names = self.model.names

        print("[INFO] Model loaded successfully")

    def detect_frame(self, frame):
        confidence = self.config["model"]["confidence_threshold"]

        results = self.model(
            frame,
            conf=confidence,
            verbose=False
        )

        detections = []

        for box in results[0].boxes:

            cls_id = int(box.cls[0])
            conf = float(box.conf[0])

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            width = x2 - x1
            height = y2 - y1

            detections.append(
                {
                    "class_id": cls_id,
                    "class_name": self.class_names[cls_id],
                    "confidence": conf,
                    "bbox": [x1, y1, x2, y2],
                    "width": width,
                    "height": height
                }
            )

        return results, detections

    def get_fps(self):
        current_time = time.time()

        time_diff = current_time - self.prev_time

        fps = 1 / time_diff if time_diff > 0 else 0

        self.prev_time = current_time

        return fps

    def draw_results(self, results):
        annotated_frame = results[0].plot()

        fps = self.get_fps()

        cv2.putText(
            annotated_frame,
            f"FPS: {fps:.1f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        return annotated_frame


def main():

    detector = Detector()

    detector.load_model()

    camera_source = detector.config["camera"]["source"]
    camera_width = detector.config["camera"]["width"]
    camera_height = detector.config["camera"]["height"]

    cap = cv2.VideoCapture(camera_source)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)

    if not cap.isOpened():
        print("[ERROR] Could not open webcam")
        return

    print("[INFO] Webcam started")
    print("[INFO] Press 'q' to quit")

    while True:

        ret, frame = cap.read()

        if not ret:
            print("[ERROR] Failed to read frame")
            break

        results, detections = detector.detect_frame(frame)

        output_frame = detector.draw_results(results)

        # Uncomment for debugging
        # for det in detections:
        #     print(
        #         f"{det['class_name']} "
        #         f"{det['confidence']:.2f}"
        #     )

        cv2.imshow(
            "Workspace Monitoring System",
            output_frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    print("[INFO] Application closed")


if __name__ == "__main__":
    main()