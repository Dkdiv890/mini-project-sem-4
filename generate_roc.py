import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
import numpy as np
import os
import sys

# Ensure AI_Training_Source_Code can be imported without issues
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from AI_Training_Source_Code.data_loader import get_datasets, get_augmentation_layer
from AI_Training_Source_Code.model import build_model, prepare_for_fine_tuning

def generate_roc():
    print("Loading datasets...")
    _, val_ds, class_names = get_datasets()
    num_classes = len(class_names)
    
    print("Building model architecture to load weights...")
    augmentation = get_augmentation_layer()
    base, _ = build_model(num_classes, augmentation)
    model = prepare_for_fine_tuning(base, _)
    
    model_path = 'best_weights.h5'
    print(f"Loading weights from {model_path}...")
    model.load_weights(model_path)
    
    print("Predicting on validation set (this may take a minute)...")
    y_true = []
    y_scores = []
    
    for images, labels in val_ds:
        preds = model.predict(images, verbose=0)
        y_true.extend(labels.numpy())
        y_scores.extend(preds)
        
    y_true = np.array(y_true)
    y_scores = np.array(y_scores)
    
    # Binarize labels for One-vs-Rest multi-class ROC
    y_true_bin = label_binarize(y_true, classes=range(num_classes))
    
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    
    plt.figure(figsize=(10, 8))
    
    colors = ['royalblue', 'darkorange', 'forestgreen']
    for i in range(num_classes):
        fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], y_scores[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
        plt.plot(fpr[i], tpr[i], color=colors[i], lw=2, 
                 label=f'{class_names[i]} (AUC = {roc_auc[i]:.3f})')

    # micro-average ROC curve
    fpr["micro"], tpr["micro"], _ = roc_curve(y_true_bin.ravel(), y_scores.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    plt.plot(fpr["micro"], tpr["micro"],
             label=f'Micro-Average (AUC = {roc_auc["micro"]:.3f})',
             color='deeppink', linestyle=':', linewidth=3)
             
    plt.plot([0, 1], [0, 1], 'k--', lw=2, label='Random Guessing')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate (FPR)', fontsize=12)
    plt.ylabel('True Positive Rate (TPR)', fontsize=12)
    plt.title('Receiver Operating Characteristic (ROC) Curve', fontsize=15, fontweight='bold')
    plt.legend(loc="lower right", fontsize=11)
    plt.grid(True, alpha=0.3)
    
    out_file = 'roc_curve.png'
    plt.savefig(out_file, dpi=150)
    print(f"Success! ROC curve saved to {out_file}")

if __name__ == '__main__':
    generate_roc()
