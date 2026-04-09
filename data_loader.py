import tensorflow as tf
from tensorflow.keras import layers
import os
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
DATASET_DIR = 'dataset'
SEED = 42

def check_dataset():
    if not os.path.exists(DATASET_DIR):
        raise FileNotFoundError(f"Dataset directory '{DATASET_DIR}' not found.\nCreate a folder named 'dataset' with subfolders: plastic, paper, metal")
    subfolders = [d for d in os.listdir(DATASET_DIR) if os.path.isdir(os.path.join(DATASET_DIR, d)) and (not d.startswith('.'))]
    if len(subfolders) == 0:
        raise FileNotFoundError(f"No class subfolders found inside '{DATASET_DIR}'.\nMake sure it contains: plastic/, paper/, metal/")
    print(f'[data_loader] Dataset structure verified. Found folders: {subfolders}')

def get_datasets():
    check_dataset()
    train_ds = tf.keras.utils.image_dataset_from_directory(DATASET_DIR, validation_split=0.2, subset='training', seed=SEED, image_size=IMG_SIZE, batch_size=BATCH_SIZE, shuffle=True)
    val_ds = tf.keras.utils.image_dataset_from_directory(DATASET_DIR, validation_split=0.2, subset='validation', seed=SEED, image_size=IMG_SIZE, batch_size=BATCH_SIZE, shuffle=True)
    class_names = train_ds.class_names
    num_classes = len(class_names)
    print(f'[data_loader] Classes found ({num_classes}): {class_names}')
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)
    return (train_ds, val_ds, class_names)

def get_augmentation_layer():
    return tf.keras.Sequential([layers.RandomFlip('horizontal'), layers.RandomRotation(0.2), layers.RandomZoom(0.1)], name='data_augmentation')