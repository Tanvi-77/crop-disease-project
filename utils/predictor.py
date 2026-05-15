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


def predict_image(image_path):

    # Read image
    img = cv2.imread(image_path)

    # Resize
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

    # Normalize
    img = img / 255.0

    # Expand dimensions
    img = np.expand_dims(img, axis=0)

    # Predict
    prediction = model.predict(img)

    predicted_index = np.argmax(prediction)

    disease = class_names[predicted_index]

    confidence = float(np.max(prediction))

    solution = solutions.get(
        disease,
        "No solution available."
    )

    return {
        "disease": disease,
        "confidence": round(confidence * 100, 2),
        "solution": solutions.get(disease, 
                                  "No solution available"
                                  )
    }