import os
import json
import numpy as np

from sklearn.model_selection import train_test_split

from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam

from preprocessing.preprocess import load_data


# =========================
# LOAD DATA
# =========================

X, y, class_names = load_data()

print("\nDataset Loaded Successfully")
print("X shape:", X.shape)
print("y shape:", y.shape)


# =========================
# ONE HOT ENCODING
# =========================

y = to_categorical(y, num_classes=len(class_names))


# =========================
# TRAIN TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTrain/Test Split Done")
print("X_train:", X_train.shape)
print("X_test :", X_test.shape)


# =========================
# LOAD MOBILENETV2
# =========================

base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

# Freeze base model
base_model.trainable = False


# =========================
# ADD CUSTOM LAYERS
# =========================

x = base_model.output
x = GlobalAveragePooling2D()(x)

x = Dense(128, activation='relu')(x)

predictions = Dense(
    len(class_names),
    activation='softmax'
)(x)

model = Model(
    inputs=base_model.input,
    outputs=predictions
)


# =========================
# COMPILE MODEL
# =========================

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("\nModel Compiled Successfully")


# =========================
# TRAIN MODEL
# =========================

history = model.fit(
    X_train,
    y_train,
    validation_data=(X_test, y_test),
    epochs=5,
    batch_size=32
)


# =========================
# SAVE MODEL
# =========================

os.makedirs("model", exist_ok=True)

model.save("model/mobilenet_model.h5")

with open("model/labels.json", "w") as f:
    json.dump(class_names, f)

print("\n✅ Model Saved Successfully")  