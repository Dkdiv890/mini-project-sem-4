import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

cm = np.array([
    [165, 2,  3],
    [ 1, 258, 4],
    [ 4,  7, 328]
])

class_names = ['Metal', 'Paper', 'Plastic']

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_names,
            yticklabels=class_names,
            linewidths=0.5, linecolor='gray',
            annot_kws={"size": 12, "weight": "bold"})
plt.title('Confusion Matrix (Validation Matrix)', fontsize=14, fontweight='bold')
plt.ylabel('True Label', fontsize=12)
plt.xlabel('Predicted Label', fontsize=12)
plt.tight_layout()
plt.savefig('validation_matrix.png', dpi=150)
print("Updated matrix to perfectly match original style!")
