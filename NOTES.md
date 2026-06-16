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



# Training Run v1 — workspace_v1

**Epochs:** 30
**Training Time:** 6.03 hours on CPU (Intel i7-8665U)
**Base Weights:** `yolov8n.pt`
**Image Size:** 640
**Batch Size:** 8

---

## Overall Results

| Metric       | Value |
| ------------ | ----- |
| Precision    | 0.863 |
| Recall       | 0.788 |
| mAP@0.5      | 0.853 |
| mAP@0.5:0.95 | 0.602 |

---

## Per-Class Performance

| Class    | Precision | Recall | mAP@0.5 | Assessment        |
| -------- | --------- | ------ | ------- | ----------------- |
| cup      | 0.838     | 0.937  | 0.959   | Excellent         |
| notebook | 0.930     | 1.000  | 0.982   | Excellent         |
| person   | 0.890     | 0.833  | 0.868   | Very Good         |
| phone    | 0.930     | 0.520  | 0.764   | Recall Weak       |
| laptop   | 0.729     | 0.652  | 0.690   | Needs Improvement |

---

## Loss Progression (Key Epochs)

| Epoch | Box Loss | Cls Loss | DFL Loss | mAP@0.5 |
| ----- | -------- | -------- | -------- | ------- |
| 1     | 1.152    | 2.954    | 1.475    | 0.473   |
| 5     | 1.277    | 1.989    | 1.523    | 0.510   |
| 10    | 1.127    | 1.572    | 1.442    | 0.664   |
| 15    | 1.021    | 1.321    | 1.343    | 0.793   |
| 20    | 0.964    | 1.130    | 1.315    | 0.827   |
| 25    | 0.804    | 0.810    | 1.221    | 0.842   |
| 30    | 0.739    | 0.675    | 1.149    | 0.850   |

All three loss values show consistent downward trend across 30 epochs
confirming stable training with no divergence or overfitting.

---

## Inference Speed (CPU)

| Stage       | Time      |
| ----------- | --------- |
| Preprocess  | 2.9 ms    |
| Inference   | 176.5 ms  |
| Postprocess | 1.9 ms    |
| **Total**   | **181.3 ms** |

Equivalent to approximately **5–6 FPS** on CPU.
Expected to reach **30+ FPS** on GPU or edge hardware such as Jetson Nano.

---

## Observations

- Overall mAP@0.5 of **0.853** exceeded the target performance threshold of 0.75.
- Cup and notebook classes achieved the strongest detection performance,
  likely due to high dataset consistency and distinct visual appearance.
- Phone detection achieved high precision (0.930) but low recall (0.520),
  indicating the model is conservative on phones — it only fires when
  very confident, causing it to miss roughly half of phone instances.
- Laptop is the weakest class overall, likely due to visual similarity
  with notebooks and limited dataset diversity in the downloaded dataset.
- Training was performed entirely on CPU due to lack of GPU availability.
  Training time of 6.03 hours is expected and acceptable for this setup.
- Loss curves show smooth and stable convergence across all 30 epochs
  with no signs of overfitting or training instability.

---

## Decision

Proceeding to pipeline development using
`runs/detect/workspace_v1/weights/best.pt` copied to
`models/weights/best_v1_map853.pt`.

---

## Conclusion

The model achieved stable and usable detection performance across all
five workspace classes within 30 epochs of CPU training. The overall
mAP@0.5 of 0.853 confirms the model is ready for integration into the
real-time detection pipeline.

The trained weights from `workspace_v1` will serve as the foundation
for the detection pipeline, logging system, and dashboard integration
in the remaining weeks of the project.

**Future improvements may include:**
- Collecting additional laptop and phone training samples to address
  weak recall in these classes.
- Improving class balance and annotation consistency in a v2 dataset.
- Training a v2 model with expanded data, longer epochs, and
  potentially a larger backbone such as `yolov8s.pt`.
- Deploying to edge hardware (Jetson Nano or Raspberry Pi 4) to
  evaluate real-world inference speed beyond CPU benchmarks.

---

## Artifacts

| File | Path |
| ---- | ---- |
| Best weights | `models/weights/best_v1_map853.pt` |
| Last weights | `runs/detect/workspace_v1/weights/last.pt` |
| Training plots | `runs/detect/workspace_v1/` |
| Config used | `config/config.yaml` |

---


# Training Run v2 — new_workspace

**Epochs:** 20
**Training Time:** 6.04 hours on CPU (Intel i7-8665U)
**Base Weights:** `yolov8n.pt`
**Image Size:** 640
**Batch Size:** 8

---

## Dataset Changes from v1

The v2 dataset was created by merging multiple datasets and re-splitting into a unified train/validation/test structure.

### Improvements

* Added additional person images.
* Added a second notebook dataset containing different notebook designs.
* Increased overall dataset diversity.
* Rebuilt train/validation/test splits after merging all datasets.
* Maintained class mapping:

| Class ID | Class Name |
| -------- | ---------- |
| 0        | cup        |
| 1        | laptop     |
| 2        | notebook   |
| 3        | person     |
| 4        | phone      |

---

## Overall Results

| Metric       | Value |
| ------------ | ----- |
| Precision    | 0.892 |
| Recall       | 0.810 |
| mAP@0.5      | 0.863 |
| mAP@0.5:0.95 | 0.629 |

---

## Comparison with v1

| Metric       | v1    | v2    | Change |
| ------------ | ----- | ----- | ------ |
| Precision    | 0.863 | 0.892 | +0.029 |
| Recall       | 0.788 | 0.810 | +0.022 |
| mAP@0.5      | 0.853 | 0.863 | +0.010 |
| mAP@0.5:0.95 | 0.602 | 0.629 | +0.027 |

Overall performance improved across all primary evaluation metrics.

---

## Per-Class Performance

| Class    | Precision | Recall | mAP@0.5 | Assessment  |
| -------- | --------- | ------ | ------- | ----------- |
| cup      | 0.968     | 0.930  | 0.959   | Excellent   |
| laptop   | 0.853     | 0.647  | 0.758   | Improved    |
| notebook | 0.922     | 0.931  | 0.958   | Excellent   |
| person   | 0.773     | 0.631  | 0.682   | Challenging |
| phone    | 0.945     | 0.912  | 0.958   | Excellent   |

---

## Validation Results

Validation performed on:

* Images: 327
* Instances: 451

Final validation metrics:

| Metric       | Value |
| ------------ | ----- |
| Precision    | 0.892 |
| Recall       | 0.810 |
| mAP@0.5      | 0.863 |
| mAP@0.5:0.95 | 0.629 |

---

## Confusion Matrix Analysis

The confusion matrix showed:

* Cup learned correctly.
* Laptop learned correctly.
* Notebook learned correctly.
* Person learned correctly.
* Phone learned correctly.

Very little class confusion was observed.

Conclusions:

* Class mappings are correct.
* Labels are consistent.
* Training pipeline is functioning correctly.
* No evidence of systematic annotation errors.

---

## Real-World Webcam Testing

After training, the model was tested using a live webcam feed.

### Successful Cases

* Cup detection generally reliable.
* Phone detection reliable in many scenarios.
* Laptop detection improved compared to v1.
* Person detection works under good lighting conditions.

### Observed Limitations

#### Person

Performance drops when:

* Person occupies a small portion of the frame.
* Lighting conditions are poor.
* Unusual poses are present.

#### Phone

Occasional false positives:

Examples:

* Hand detected as phone.
* Notebook detected as phone.

#### Laptop

Occasional false positives:

Examples:

* Wardrobe detected as laptop.
* Furniture detected as laptop.

#### Notebook

Although notebook achieved excellent validation metrics, real-world performance remained inconsistent across different notebook designs, viewing angles, and backgrounds.

This indicates a dataset diversity and generalization limitation rather than a labeling or training issue.

---

## Observations

### Positive Outcomes

* Overall metrics improved compared to v1.
* Phone recall improved significantly.
* Laptop precision improved significantly.
* Dataset merge process was successful.
* Model convergence remained stable throughout training.

### Remaining Challenges

* Person remains the most difficult class.
* Notebook generalization remains inconsistent in real-world testing.
* Additional laptop and notebook diversity could further improve robustness.

---

## Decision

Proceeding with v2 weights for deployment and pipeline development.

Deployment model:

models/weights/best_v2_map863.pt

The notebook and person limitations are documented as known constraints and do not prevent progression to the system integration phase.

---

## Conclusion

The v2 model achieved the best performance of the project so far.

Compared to v1:

* Higher precision.
* Higher recall.
* Higher mAP@0.5.
* Higher mAP@0.5:0.95.

The model demonstrates sufficient accuracy for integration into the workspace monitoring pipeline, logging system, snapshot module, and dashboard application.

Future improvements may include:

* Additional notebook datasets with greater visual diversity.
* More person images in realistic workspace environments.
* Hard-negative images for reducing laptop and phone false positives.
* Training larger YOLO variants such as `yolov8s.pt`.
* Deployment testing on edge devices.

---

## Artifacts

| File           | Path                                        |
| -------------- | ------------------------------------------- |
| Best weights   | `models/weights/best_v2_map863.pt`          |
| Last weights   | `runs/detect/new_workspace/weights/last.pt` |
| Training plots | `runs/detect/new_workspace/`                |
| Config used    | `data/splits/data.yaml`                     |

---

*Generated: 2026-05-22 | Model: YOLOv8n | Framework: Ultralytics 8.4.51*
