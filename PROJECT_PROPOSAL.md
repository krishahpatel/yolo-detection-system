# Workspace Monitoring System

## Project Title
Workspace Monitoring System using YOLOv8

---

## Problem Statement
Workstations in offices and labs often require monitoring to determine
occupancy and object presence. Manual monitoring is inefficient and
difficult to scale. This leads to wasted resources, security gaps, and
no visibility into workspace utilization patterns.

---

## Proposed Solution
Develop a real-time object detection system using YOLOv8 that monitors
workspace objects and occupancy through a live webcam feed, logs all
detections to a database, and displays live statistics on a web dashboard.

---

## Classes to Detect
- person
- laptop
- phone
- notebook
- cup

---

## Tech Stack
- YOLOv8 (Ultralytics) — detection model
- Python 3.10 — core language
- OpenCV — webcam capture and frame processing
- SQLite — detection logging
- Streamlit — live dashboard
- Roboflow — data annotation and augmentation

---

## Data Collection
Images will be collected using a laptop webcam under varied lighting
conditions, angles, distances, and backgrounds. Target: 250–300 images
per class, totalling approximately 1,250–1,500 images.

---

## Final System Features
- Real-time object detection via webcam
- Bounding box and confidence score visualization
- Detection event logging with timestamps to SQLite
- Snapshot saving on high-confidence detections
- Desktop alert notifications
- Live web dashboard with statistics and detection history

---

## Success Metrics
- Target mAP@0.5: 0.75 or higher
- Real-time inference at minimum 15 FPS on laptop CPU
- Low false positive rate (under 10% on test set)
- Dashboard accessible from any device on local network

---

## Rough Timeline

| Week | Focus | End-of-week Deliverable |
|------|-------|------------------------|
| 1 | Setup + Data | Annotated dataset ready for training |
| 2 | Training | Trained model with mAP above 0.75 |
| 3 | Pipeline | Real-time detection and logging working |
| 4 | Dashboard | Live dashboard accessible on network |
| 5 | Polish + Demo | GitHub repo, demo video, presentation |