# 🌱 Crop Disease Detection System using Machine Learning

An AI-powered web application that detects crop diseases from leaf images using **MobileNetV2 Transfer Learning**. Users can upload a leaf image, and the system predicts the disease, displays the confidence score, and recommends suitable treatments through a rule-based recommendation system.

---

## 📌 Project Overview

Crop diseases can significantly reduce agricultural productivity if they are not identified early. This project aims to help farmers and agriculture enthusiasts detect plant diseases quickly by analyzing leaf images using a deep learning model.

The application is built with **Python** and **Streamlit**, making it simple and interactive. After predicting the disease, the system also provides treatment recommendations and stores prediction history in a SQLite database.

---

## ✨ Features

- Upload crop leaf images
- Image preprocessing before prediction
- Disease detection using MobileNetV2
- Confidence score for every prediction
- Rule-based treatment recommendations
- Prediction history stored in SQLite
- Simple and responsive Streamlit interface
- Multi-language support (English, Hindi, Marathi)

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| Deep Learning | TensorFlow, Keras |
| Model | MobileNetV2 (Transfer Learning) |
| Frontend | Streamlit |
| Database | SQLite |
| Image Processing | OpenCV, Pillow |
| Data Handling | NumPy, Pandas |
| Visualization | Matplotlib |

---


## ⚙️ Working Flow


User Uploads Leaf Image
            │
            ▼
 Image Preprocessing
            │
            ▼
 MobileNetV2 Model
            │
            ▼
 Disease Prediction
            │
            ▼
 Confidence Score
            │
            ▼
 Treatment Recommendation
            │
            ▼
 Store Result in SQLite
            │
            ▼
 Display Result on Streamlit


---

## 📊 Supported Crop Classes

### 🍅 Tomato
- Healthy
- Early Blight
- Late Blight

### 🥔 Potato
- Healthy
- Early Blight
- Late Blight

### 🫑 Pepper
- Healthy
- Bacterial Spot

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Crop-Disease-Detection.git
cd Crop-Disease-Detection
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
streamlit run app/app.py
```

---

## 💾 Database

SQLite is used to store:

- Prediction history
- Disease name
- Confidence score
- Timestamp

---

## 📸 Future Enhancements

- Support more crop varieties
- Real-time camera detection
- Cloud database integration
- Weather-based disease prediction
- Fertilizer recommendation
- Mobile application

---

## 👩‍💻 Author

**Tanvi Salaskar**
MCA Student

---

## ⭐ If you found this project useful, don't forget to give it a star!
