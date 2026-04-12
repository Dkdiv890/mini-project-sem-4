---
title: WasteAI Intelligent Classifier
emoji: ♻️
colorFrom: green
colorTo: green
sdk: docker
pinned: false
---

<div align="center">
  <img src="https://img.icons8.com/isometric/512/bothe-recycle-bin.png" width="120" />
  <h1>♻️ WasteAI: Intelligent Waste Classifier</h1>
  <p><strong>A Premium Deep Learning Engine for Real-Time Waste Segregation</strong></p>
  
  [![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
  [![TensorFlow 2.12](https://img.shields.io/badge/TensorFlow-2.12-orange.svg?style=flat-square&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
  [![Flask](https://img.shields.io/badge/Flask-Web_UI-000000.svg?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
  [![EfficientNetB0](https://img.shields.io/badge/Architecture-EfficientNetB0-green.svg?style=flat-square)](https://arxiv.org/abs/1905.11946)
</div>

---

## 🌟 Project Overview
WasteAI is a state-of-the-art computer vision application designed to automate the classification of common### 📊 Dataset Details
- **Source**: [Kaggle - Garbage Classification V2](https://www.kaggle.com/datasets/sumn2u/garbage-classification-v2)
- **Total Images**: ~3,800
- **Classes**: Metal, Paper, Plastic
. 

Built for industrial-grade reliability, the system leverages **Transfer Learning** with the **EfficientNetB0** architecture, trained on thousands of verified real-world samples to achieve an impressive **96% validation accuracy**.

### ✨ Highlights
- **Premium Dark-Mode UI:** A modern, glassmorphism-inspired web interface built with Flask and Vanilla CSS/JS.
- **EfficientNetB0 Power:** High-accuracy classification with low computational overhead, optimized for cloud deployment.
- **Real-Time Analysis:** Instant results with confidence scoring and recycling tips.
- **Production-Ready:** Fully configured for deployment on Render.com with memory-optimized startup logic.

---

## 🚀 Experience the UI
The new web interface features:
- 🎯 **Drag & Drop** image uploads.
- 📊 **Animated Confidence Bars** showing the top 3 predictions.
- 💡 **Smart Recycling Tips** based on the identified material.
- 📱 **Fully Responsive** design for mobile and desktop presentation.

---

## 🛠️ Technical Implementation

### Model Architecture
The engine utilizes **EfficientNetB0**, which uses a compound scaling method to balance network depth and width. 
- **Training Strategy:** Two-phase approach (Frozen Feature Extraction + Fine-Tuning).
- **Optimization:** Adam optimizer with `ReduceLROnPlateau` and `EarlyStopping` callbacks.
- **Accuracy:** `~96%` on the verified dataset.

### Deployment Stack
- **Backend:** Flask (Python)
- **Production Server:** Gunicorn (Optimized with 1 worker/4 threads for Render Free Tier)
- **Environment:** `tensorflow-cpu` to fit within 512MB RAM limits.

---

## 💻 Running Locally

1. **Clone & Setup:**
   ```bash
   git clone https://github.com/Dkdiv890/Mini-Project-4-sem.git
   cd "alok gn"
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch:**
   ```bash
   python app.py
   ```
   *Visit `http://127.0.0.1:8080` in your browser.*

---

## 📂 Project Structure
- `app.py`: Flask API & Model Loading Logic
- `templates/`: HTML structures
- `static/`: Modern CSS & JS logic
- `waste_classification_model.h5`: The "Brain" (Trained Neural Network)
- `AI_Training_Source_Code/`: Original training scripts and data loaders

---
<div align="center">
  <sub>Developed with ❤️ for Academic Excellence in AI & Machine Learning.</sub>
</div>
