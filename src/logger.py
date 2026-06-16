import sqlite3
import time
from datetime import datetime


class DetectionLogger:
    def __init__(self, db_path="logs/detections.db"):

        self.conn = sqlite3.connect(db_path)

        self.cursor = self.conn.cursor()

        self.last_logged = {}

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            class_name TEXT,
            confidence REAL,
            bbox_x REAL,
            bbox_y REAL,
            bbox_w REAL,
            bbox_h REAL
        )
        """)

        self.conn.commit()

    def log_detection(
        self,
        class_name,
        confidence,
        bbox
    ):

        current_time = time.time()

        if class_name in self.last_logged:
            if current_time - self.last_logged[class_name] < 10:
                return

        self.last_logged[class_name] = current_time

        x, y, w, h = bbox

        self.cursor.execute("""
        INSERT INTO detections
        (
            timestamp,
            class_name,
            confidence,
            bbox_x,
            bbox_y,
            bbox_w,
            bbox_h
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            class_name,
            float(confidence),
            float(x),
            float(y),
            float(w),
            float(h)
        ))

        self.conn.commit()

    def get_recent(self, limit=10):

        self.cursor.execute("""
        SELECT *
        FROM detections
        ORDER BY id DESC
        LIMIT ?
        """, (limit,))

        return self.cursor.fetchall()

    def get_counts_by_class(self):

        self.cursor.execute("""
        SELECT class_name, COUNT(*)
        FROM detections
        GROUP BY class_name
        """)

        return self.cursor.fetchall()

    def close(self):
        self.conn.close()