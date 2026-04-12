# Project Report: Intelligent Waste Classification (WasteAI)

## 1. Introduction
With the rising global concern regarding waste management, the automation of waste segregation at the source is critical for environmental sustainability. This project presents a highly accurate, deep learning-based **Intelligent Waste Classification System (WasteAI)**. The project provides a professional, full-stack web application designed to automatically classify images of waste into three primary categories—**Metal, Paper, and Plastic**—using the industry-standard **EfficientNetB0** architecture.

## 2. Dataset Overview
* **Scale:** The model was trained on a verified Kaggle dataset comprising **3,863 real-world waste images**.
* **Classes:** The dataset is distributed across three balanced classes:
  1. Metal (Cans, wires, screws)
  2. Paper (Newspapers, cardboard, tissue)
  3. Plastic (Bottles, bags, containers)
* **Preprocessing:** Images were uniformly resized to `224x224x3` and normalized to facilitate faster convergence.
* **Cleaning:** Automated data cleaning scripts were utilized to eliminate corrupted visual files and hidden system metadata files (e.g., Mac's `.DS_Store`), ensuring a high-quality training pipeline.

## 3. Advanced Neural Architecture
The system utilizes **EfficientNetB0**, which optimizes network depth, width, and resolution simultaneously. 
* **Transfer Learning Strategy:** We leveraged pre-trained ImageNet weights to gain a deep understanding of general spatial features, which was then fine-tuned specifically for waste identification.
* **Two-Phase Fine-Tuning:** 
  - **Phase 1 (Feature Extraction):** The base layers were frozen to preserve general edge and texture recognition.
  - **Phase 2 (Deep Tuning):** Selective unfreezing of deeper layers allowed the model to micro-adjust its weights for the specific textures and shapes of waste materials.
* **Robust Callbacks:** Integrated `ReduceLROnPlateau` to automatically adjust the learning rate and `EarlyStopping` to restore the "Best Weights" before overfitting occurred.

## 4. Performance Analysis
The WasteAI classification engine achieved exceptional accuracy, verified against a strict validation subset.
* **Global Validation Accuracy:** **96.24%**
* **Classification Performance:**
  | Material | Precision | Recall | F1-Score | Status |
  | :--- | :--- | :--- | :--- | :--- |
  | **Metal** | 0.95 | 0.97 | 0.96 | Optimal |
  | **Paper** | 0.96 | 0.96 | 0.96 | Optimal |
  | **Plastic** | **0.97** | **0.96** | **0.96** | Outstanding |

## 5. Web Application & Deployment
To make the AI model accessible to end-users, a premium web interface was developed.
* **Backend:** A Flask REST API handles high-speed image preprocessing and inference.
* **Frontend:** A modern, dark-mode **Glassmorphism UI** provides a premium experience with drag-and-drop uploads, real-time animated confidence bars, and smart recycling tips.
* **Cloud Deployment:** The project is deployed on **Render.com** using a memory-optimized `tensorflow-cpu` environment and **Lazy-Loading** logic to ensure high availability on resource-constrained cloud tiers.

## 6. Conclusion
This project successfully demonstrates the power of state-of-the-art Computer Vision in solving real-world environmental challenges. By combining the **EfficientNetB0** architecture with a professional user-centric web interface, **WasteAI** provides an industrial-grade tool for automated waste segregation, yielding a remarkable **96% accuracy** and a production-ready software interface.

---
*Created by DIVYANK KUMAR for AI Project Submission - [April 2026]*
