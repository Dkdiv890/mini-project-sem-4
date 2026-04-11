<div align="center">
  <h1>♻️ Intelligent Waste Classification AI</h1>
  <p><strong>A Deep Learning Computer Vision engine capable of predicting Metal, Paper, and Plastic waste in real-time with 98% validated accuracy.</strong></p>
  
  [![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
  [![TensorFlow](https://img.shields.io/badge/TensorFlow-2.19.0-orange.svg)](https://www.tensorflow.org/)
  [![Gradio](https://img.shields.io/badge/Gradio-Web_UI-ff69b4.svg)](https://gradio.app/)
  [![Deployment](https://img.shields.io/badge/Cloud-Render-purple.svg)](https://render.com/)
</div>

<br />

## 🌟 Overview
Solving empirical challenges in automated waste segregation at an industrial robotic level. This repository contains a production-ready artificial intelligence engine configured to reliably scrutinize and classify raw object instances into actionable categorical outcomes.

Trained extensively locally (by leveraging Transfer Learning & the **EfficientNetB0** architecture) across ~6,000 augmented empirical images, the system yields unparalleled operational accuracy without extensive computational overhead.

## 🛠️ Technology Stack
* **AI & Deep Learning:** TensorFlow, Keras, EfficientNetB0
* **Data Processing:** Pillow (PIL), NumPy, OS Walk/Regex pipelines
* **Web Interface:** Gradio (Rapid HuggingFace Frontend API)
* **Deployment & Cloud:** Procfile, Render.com

---

## 📈 Model Performance & Accuracy Metrics
The model utilizes a heavily researched Two-Phase Deep Training mechanism (Broad Feature Extraction mapping followed by Unfrozen Deep-Parameter Fine-tuning on 58 hidden layers).

**Global Validated Accuracy:** `98.11%`

| Class Target   | Precision      | Recall    | F1-Score |
| -------------- | -------------- | --------- | -------- |
| **Metal**      | 97%            | 98%       | 97%      |
| **Paper**      | 97%            | 98%       | 97%      |
| **Plastic**    | **99%**        | **97%**   | **98%**  |

---

## 💻 How to Run Locally
Want to test the AI on your local machine rather than the cloud infrastructure? Follow these simple steps.

**1. Clone the Repository:**
```bash
git clone https://github.com/Dkdiv890/pookies.git
cd pookies
```

**2. Setup Python Virtual Environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
```

**3. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**4. Launch the Web UI Server:**
```bash
python app.py
```
> The terminal will provide a Local URL (e.g., `http://127.0.0.1:xxxx`). Open it in Chrome and interact with the AI directly!

---

## ☁️ Cloud Deployment (Render.com)
The platform is fully configured for automatic continuous deployment. To re-deploy to Render:
1. Ensure your latest `waste_classification_model.h5`, `app.py`, and `requirements.txt` are pushed here.
2. Render automatically detects the configuration and uses the `Procfile` command `web: python app.py`.
3. The platform binds the Gradio port independently. Done!

---
*Developed proudly as a Computer Vision classification demonstration.*
