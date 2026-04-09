import tensorflow as tf
print('TensorFlow version:', tf.__version__)
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f'✅  GPU detected: {gpus}')
else:
    print('⚠️  No GPU found — Go to Runtime → Change Runtime Type → GPU')
from google.colab import files
import zipfile, os
print('Select your dataset.zip file...')
uploaded = files.upload()
zip_name = list(uploaded.keys())[0]
print(f"\nExtracting '{zip_name}' ...")
with zipfile.ZipFile(zip_name, 'r') as zip_ref:
    zip_ref.extractall('.')
DATASET_DIR = None
for entry in os.listdir('.'):
    if os.path.isdir(entry) and entry not in ['sample_data', '__pycache__']:
        subfolders = [d for d in os.listdir(entry) if os.path.isdir(os.path.join(entry, d))]
        if len(subfolders) >= 3:
            DATASET_DIR = entry
            break
if DATASET_DIR is None:
    DATASET_DIR = 'dataset'
print(f"\n✅  Dataset extracted! Using folder: '{DATASET_DIR}/'")
subfolders = [d for d in os.listdir(DATASET_DIR) if not d.startswith('.')]
for folder in subfolders:
    count = len(os.listdir(os.path.join(DATASET_DIR, folder)))
    print(f'   {folder}/  →  {count} images')
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS_PHASE1 = 10
EPOCHS_PHASE2 = 10
SEED = 42
MODEL_SAVE = 'waste_classification_model.h5'
print('Configuration:')
print(f'  Image size   : {IMG_SIZE}')
print(f'  Batch size   : {BATCH_SIZE}')
print(f'  Phase 1 epochs : {EPOCHS_PHASE1}  (base frozen)')
print(f'  Phase 2 epochs : {EPOCHS_PHASE2}  (fine-tuning)')
from tensorflow.keras import layers
train_ds = tf.keras.utils.image_dataset_from_directory(DATASET_DIR, validation_split=0.2, subset='training', seed=SEED, image_size=IMG_SIZE, batch_size=BATCH_SIZE, shuffle=True)
val_ds = tf.keras.utils.image_dataset_from_directory(DATASET_DIR, validation_split=0.2, subset='validation', seed=SEED, image_size=IMG_SIZE, batch_size=BATCH_SIZE, shuffle=True)
class_names = train_ds.class_names
NUM_CLASSES = len(class_names)
print(f'\nClasses ({NUM_CLASSES}): {class_names}')
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)
augmentation = tf.keras.Sequential([layers.RandomFlip('horizontal'), layers.RandomRotation(0.2), layers.RandomZoom(0.1)], name='data_augmentation')
print('✅  Dataset loaded and ready.')
from tensorflow.keras import models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
base_model = MobileNetV2(input_shape=IMG_SIZE + (3,), include_top=False, weights='imagenet')
base_model.trainable = False
print(f'Base model: {len(base_model.layers)} layers — all FROZEN for Phase 1')
inputs = tf.keras.Input(shape=IMG_SIZE + (3,), name='input_image')
x = augmentation(inputs)
x = preprocess_input(x)
x = base_model(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.2)(x)
outputs = layers.Dense(NUM_CLASSES, activation='softmax', name='output')(x)
model = models.Model(inputs, outputs, name='WasteClassifier')
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001), loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=['accuracy'])
model.summary()
print(f"\n{'=' * 50}")
print(f'  Phase 1: Feature Extraction  ({EPOCHS_PHASE1} epochs)')
print(f"{'=' * 50}")
history1 = model.fit(train_ds, epochs=EPOCHS_PHASE1, validation_data=val_ds)
print(f"\nPhase 1 done. Val accuracy: {history1.history['val_accuracy'][-1]:.4f}")
print(f"\n{'=' * 50}")
print(f'  Phase 2: Fine-Tuning  ({EPOCHS_PHASE2} more epochs)')
print(f"{'=' * 50}")
base_model.trainable = True
FREEZE_UNTIL = 100
for layer in base_model.layers[:FREEZE_UNTIL]:
    layer.trainable = False
unfrozen = sum((1 for l in base_model.layers if l.trainable))
print(f'Unfrozen base layers: {unfrozen}  (first {FREEZE_UNTIL} remain frozen)')
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-05), loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=['accuracy'])
history2 = model.fit(train_ds, epochs=EPOCHS_PHASE1 + EPOCHS_PHASE2, initial_epoch=history1.epoch[-1] + 1, validation_data=val_ds)
print(f"\nPhase 2 done. Val accuracy: {history2.history['val_accuracy'][-1]:.4f}")
model.save(MODEL_SAVE)
print(f"✅  Model saved → '{MODEL_SAVE}'")
files.download(MODEL_SAVE)
print('📥  Model download started to your Mac!')
import matplotlib.pyplot as plt
acc = history1.history['accuracy'] + history2.history['accuracy']
val_acc = history1.history['val_accuracy'] + history2.history['val_accuracy']
loss = history1.history['loss'] + history2.history['loss']
val_loss = history1.history['val_loss'] + history2.history['val_loss']
plt.figure(figsize=(10, 8))
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy', color='royalblue')
plt.plot(val_acc, label='Validation Accuracy', color='darkorange')
plt.axvline(EPOCHS_PHASE1 - 1, linestyle='--', color='gray', label='Fine-Tuning Starts')
plt.ylabel('Accuracy')
plt.title('Training vs Validation Accuracy')
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)
plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss', color='royalblue')
plt.plot(val_loss, label='Validation Loss', color='darkorange')
plt.axvline(EPOCHS_PHASE1 - 1, linestyle='--', color='gray', label='Fine-Tuning Starts')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.title('Training vs Validation Loss')
plt.legend(loc='upper right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('performance_evaluation.png', dpi=150)
plt.show()
files.download('performance_evaluation.png')
print('📥  Plot downloaded to your Mac!')
import numpy as np
from sklearn.metrics import classification_report
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
files.download('classification_report.txt')
print('📥  Classification report downloaded to your Mac!')
print('\n' + '=' * 50)
print('  🎉  Training Complete!')
print(f'  ✔  Val Accuracy : {val_acc[-1] * 100:.2f}%')
print(f'  ✔  Model        → {MODEL_SAVE}')
print(f'  ✔  Plot         → performance_evaluation.png')
print(f'  ✔  Report       → classification_report.txt')
print('=' * 50)