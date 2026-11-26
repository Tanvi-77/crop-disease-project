import json
import numpy as np
import cv2

from tensorflow.keras.models import load_model

from utils.solution_mapper import solutions


# =========================
# LOAD MODEL
# =========================

model = load_model("model/mobilenet_model.h5")

with open("model/labels.json", "r") as f:
    class_names = json.load(f)


# =========================
# PREDICTION FUNCTION
# =========================

IMG_SIZE = 224


def preprocess_image(image_path):
    """Read and preprocess an image identically to the trained classifier."""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Unable to read image from path: {image_path}")

    resized = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    normalized = resized / 255.0
    batched = np.expand_dims(normalized, axis=0)
    return batched, img


def get_model():
    """Return the already-loaded Keras model without reloading."""
    return model


def predict_image(image_path):

    img, _ = preprocess_image(image_path)

    # Predict
    prediction = model.predict(img)

    predicted_index = int(np.argmax(prediction))

    disease = class_names[predicted_index]

    confidence = float(np.max(prediction))

    solution = solutions.get(
        disease,
        "No solution available."
    )

    return {
        "disease": disease,
        "confidence": round(confidence * 100, 2),
        "solution": solution
    }