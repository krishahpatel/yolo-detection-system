# YOLO Learning Notes

## Test Image — Laptop Image

### Detection Results
YOLO successfully detected a laptop object in the image.

### Bounding Box Output
[130.5385,  30.1228, 856.7325, 640.2915]

Meaning:
- x1 → left edge of object
- y1 → top edge of object
- x2 → right edge of object
- y2 → bottom edge of object

The bounding box creates a rectangle around the detected object.

### Confidence Score
Example confidence:
0.78

This means the model is 78% confident that the detected object is a cell phone.

### Class ID
Example:
63

The class ID corresponds to the object category in the COCO dataset.

### Class Name
Example: laptop

YOLO maps class IDs to readable object names using the COCO class dictionary.

---

# Observations

- YOLO detected the laptop correctly.
- Confidence was high because the object was clearly visible.
- Bright lighting improved detection accuracy.
- Large and centered objects are easier to detect.
- Small or partially hidden objects may reduce confidence.

---

# Things Learned

- YOLO returns object locations using pixel coordinates.
- Confidence scores indicate prediction certainty.
- Object detection includes both classification and localization.
- Different image conditions affect detection performance.
