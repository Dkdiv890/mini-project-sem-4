import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import os
MODEL_PATH = 'waste_classification_model.h5'

def plot_history(history_phase1, history_phase2, epochs_phase1):
    acc = history_phase1.history['accuracy'] + history_phase2.history['accuracy']
    val_acc = history_phase1.history['val_accuracy'] + history_phase2.history['val_accuracy']
    loss = history_phase1.history['loss'] + history_phase2.history['loss']
    val_loss = history_phase1.history['val_loss'] + history_phase2.history['val_loss']
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    plt.plot(acc, label='Training Accuracy', color='royalblue')
    plt.plot(val_acc, label='Validation Accuracy', color='darkorange')
    plt.axvline(epochs_phase1 - 1, linestyle='--', color='gray', label='Fine-Tuning Starts')
    plt.ylabel('Accuracy')
    plt.title('Training vs Validation Accuracy')
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    plt.subplot(2, 1, 2)
    plt.plot(loss, label='Training Loss', color='royalblue')
    plt.plot(val_loss, label='Validation Loss', color='darkorange')
    plt.axvline(epochs_phase1 - 1, linestyle='--', color='gray', label='Fine-Tuning Starts')
    plt.ylabel('Loss (Cross Entropy)')
    plt.xlabel('Epoch')
    plt.title('Training vs Validation Loss')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('performance_evaluation.png', dpi=150)
    print("[evaluate] Plot saved → 'performance_evaluation.png'")

def evaluate_and_report(val_ds, class_names):
    if not os.path.exists(MODEL_PATH):
        print(f"[evaluate] Model file '{MODEL_PATH}' not found. Skipping report.")
        return
    model = tf.keras.models.load_model(MODEL_PATH)
    print(f"[evaluate] Model loaded from '{MODEL_PATH}'")
    y_true, y_pred = ([], [])
    for images, labels in val_ds:
        preds = model.predict(images, verbose=0)
        y_true.extend(labels.numpy())
        y_pred.extend(np.argmax(preds, axis=1))
    report = classification_report(y_true, y_pred, target_names=class_names)
    print('\n── Classification Report ──────────────────────')
    print(report)
    with open('classification_report.txt', 'w') as f:
        f.write(report)
    print("[evaluate] Classification report saved → 'classification_report.txt'")