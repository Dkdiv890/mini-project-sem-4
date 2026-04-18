import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

cm = np.array([
    [165, 2,  3],
    [ 1, 258, 4],
    [ 4,  7, 328]
])

class_names = ['Metal', 'Paper', 'Plastic']

# Adjusted figure size closer to a square (7x6) to avoid massive white spaces
plt.figure(figsize=(7, 6))

# Added square=True to ensure perfect visual symmetry of the boxes
ax = sns.heatmap(cm, annot=False, cmap='Blues',
            xticklabels=class_names,
            yticklabels=class_names,
            linewidths=0.5, linecolor='gray',
            square=True) 

for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        value = cm[i, j]
        text_color = "white" if value > 100 else "black"
        ax.text(j + 0.5, i + 0.5, str(value),
                ha="center", va="center", color=text_color,
                fontsize=14, fontweight="bold")

plt.title('Validation Confusion Matrix', fontsize=14, fontweight='bold', pad=15)
plt.ylabel('True Label', fontsize=12)
plt.xlabel('Predicted Label', fontsize=12)
plt.tight_layout()
plt.savefig('validation_matrix.png', dpi=150)
print("Square symmetric matrix generated!")
