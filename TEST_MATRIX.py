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

# Plot the heatmap without seaborn annotations
ax = sns.heatmap(cm, annot=False, cmap='Blues',
            xticklabels=class_names,
            yticklabels=class_names,
            linewidths=0.5, linecolor='gray')

# Manually add the text to guarantee it shows up properly in all rows
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        # Decide text color based on cell color (dark background needs white text)
        value = cm[i, j]
        # Rough heuristic: if value > 100, background is dark blue -> text white
        text_color = "white" if value > 100 else "black"
        ax.text(j + 0.5, i + 0.5, str(value),
                ha="center", va="center", color=text_color,
                fontsize=14, fontweight="bold")

plt.title('Validation Confusion Matrix', fontsize=14, fontweight='bold')
plt.ylabel('True Label', fontsize=12)
plt.xlabel('Predicted Label', fontsize=12)
plt.tight_layout()
plt.savefig('TEST_MATRIX.png', dpi=150)
plt.savefig('validation_matrix.png', dpi=150)
print("Manual text matrix generated!")
