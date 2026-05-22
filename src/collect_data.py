import cv2
import os
import time
import argparse

def collect_images(class_name, save_dir="data/raw", target_count=300):
    class_dir = os.path.join(save_dir, class_name)
    os.makedirs(class_dir, exist_ok=True)

    existing = len([f for f in os.listdir(class_dir) if f.endswith('.jpg')])
    count = existing

    print(f"\nCollecting images for class: '{class_name}'")
    print(f"Already collected: {existing} | Target: {target_count}")
    print("Controls: SPACE = save frame | Q = quit | R = show remaining\n")

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Cannot read from webcam.")
            break

        remaining = target_count - count
        display = frame.copy()

        cv2.putText(display, f"Class: {class_name}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(display, f"Saved: {count} / {target_count}", (10, 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(display, "SPACE: Save | Q: Quit", (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)

        cv2.imshow("Data Collection", display)
        key = cv2.waitKey(1) & 0xFF

        if key == ord(' '):
            filename = os.path.join(class_dir, f"{class_name}_{int(time.time())}_{count:04d}.jpg")
            cv2.imwrite(filename, frame)
            count += 1
            print(f"Saved {count}/{target_count}: {filename}")

            if count >= target_count:
                print(f"\nTarget reached for '{class_name}'!")
                break

        elif key == ord('q'):
            print(f"\nStopped early. Collected {count} images for '{class_name}'.")
            break

    cap.release()
    cv2.destroyAllWindows()
    return count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--class_name", type=str, required=True, help="Name of the class to collect")
    parser.add_argument("--target", type=int, default=300, help="Number of images to collect")
    args = parser.parse_args()

    collect_images(args.class_name, target_count=args.target)