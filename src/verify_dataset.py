import os
import yaml

def verify_dataset(data_yaml_path="data/splits/data.yaml"):
    with open(data_yaml_path, 'r') as f:
        config = yaml.safe_load(f)

    base_path = config.get("path", "")

    print("\n--- Dataset Verification Report ---\n")

    splits = ['train', 'val', 'test']

    for split in splits:
        img_path = os.path.join(base_path, config[split])
        lbl_path = img_path.replace("images", "labels")

        images = [f for f in os.listdir(img_path)
                  if f.endswith(('.jpg', '.png', '.jpeg'))]

        labels = [f for f in os.listdir(lbl_path)
                  if f.endswith('.txt')]

        print(f"{split.upper()}:")
        print(f"Images: {len(images)}")
        print(f"Labels: {len(labels)}")

        if len(images) == len(labels):
            print("[OK] Counts match\n")
        else:
            print("[WARNING] Counts mismatch\n")

if __name__ == "__main__":
    verify_dataset()