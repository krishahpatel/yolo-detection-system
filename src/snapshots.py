import os
import cv2
from datetime import datetime


class SnapshotManager:

    def __init__(self, snapshot_dir="snapshots"):
        self.snapshot_dir = snapshot_dir
        os.makedirs(self.snapshot_dir, exist_ok=True)

    def save_snapshot(self, frame, class_name):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = f"{class_name}_{timestamp}.jpg"

        filepath = os.path.join(
            self.snapshot_dir,
            filename
        )

        cv2.imwrite(filepath, frame)

        return filepath