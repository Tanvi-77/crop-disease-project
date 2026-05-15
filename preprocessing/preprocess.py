import os
import cv2
import numpy as np

DATASET_PATH = "dataset/raw"
IMG_SIZE = 224
IMAGES_PER_CLASS = 400


def load_data():
    data = []
    labels = []
    class_names = sorted(os.listdir(DATASET_PATH))  # sorted for consistency

    for label, class_name in enumerate(class_names):
        class_path = os.path.join(DATASET_PATH, class_name)

        if not os.path.isdir(class_path):
            continue

        images = os.listdir(class_path)[:IMAGES_PER_CLASS]

        print(f"Processing {class_name} ({len(images)} images)")

        for img_name in images:
            img_path = os.path.join(class_path, img_name)

            try:
                img = cv2.imread(img_path)
                if img is None:
                    continue

                img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
                img = img / 255.0

                data.append(img)
                labels.append(label)

            except Exception as e:
                print(f"Error: {img_name}")
                continue

    return np.array(data), np.array(labels), class_names


if __name__ == "__main__":
    X, y, classes = load_data()

    print("\n✅ DONE")
    print("Data shape:", X.shape)
    print("Labels shape:", y.shape)
    print("Classes:", classes)