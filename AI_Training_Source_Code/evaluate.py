import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import os

MODEL_PATH = 'waste_classification_model'

def plot_history(history_phase1, history_phase2, epochs_phase1):
    acc = history_phase1.history['accuracy'] + history_phase2.history['accuracy']
    val_acc = history_phase1.history['val_accuracy'] + history_phase2.history['val_accuracy']
    loss = history_phase1.history['loss'] + history_phase2.history['loss']
    val_loss = history_phase1.history['val_loss'] + history_phase2.history['val_loss']
    
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    plt.plot(acc, label='Training Accuracy', color='royalblue')
    plt.plot(val_acc, label='Validation Accuracy', color='darkorange')
    plt.axvline(epochs_phase1 - 1, linestyle='--', color='gray')
    plt.ylabel('Accuracy')
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 1, 2)
    plt.plot(loss, label='Training Loss', color='royalblue')
    plt.plot(val_loss, label='Validation Loss', color='darkorange')
    plt.axvline(epochs_phase1 - 1, linestyle='--', color='gray')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('performance_evaluation.png', dpi=150)

def evaluate_and_report(val_ds, class_names):
    if not os.path.exists(MODEL_PATH):
        return
        
    model = tf.keras.models.load_model(MODEL_PATH)
    y_true, y_pred = ([], [])
    for images, labels in val_ds:
        preds = model.predict(images, verbose=0)
        y_true.extend(labels.numpy())
        y_pred.extend(np.argmax(preds, axis=1))
    
    report = classification_report(y_true, y_pred, target_names=class_names)
    with open('classification_report.txt', 'w') as f:
        f.write(report)
    print(report)
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names,
                yticklabels=class_names,
                linewidths=0.5, linecolor='gray')
    plt.title('Confusion Matrix (Validation Matrix)', fontsize=14, fontweight='bold')
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=150)
    print("[✓] Confusion matrix saved → confusion_matrix.png")
