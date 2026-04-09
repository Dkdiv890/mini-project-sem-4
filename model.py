import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
IMG_SIZE = (224, 224)
FREEZE_UNTIL = 100
LR_PHASE1 = 0.0001
LR_PHASE2 = 1e-05

def build_model(num_classes: int, augmentation_layer):
    base_model = MobileNetV2(input_shape=IMG_SIZE + (3,), include_top=False, weights='imagenet')
    base_model.trainable = False
    print(f'[model] Base model loaded. Total layers: {len(base_model.layers)}')
    print(f'[model] Base layers FROZEN for Phase-1 training.')
    inputs = tf.keras.Input(shape=IMG_SIZE + (3,), name='input_image')
    x = augmentation_layer(inputs)
    x = preprocess_input(x)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation='softmax', name='output')(x)
    model = models.Model(inputs, outputs, name='WasteClassifier_Phase1')
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=LR_PHASE1), loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=['accuracy'])
    return (model, base_model)

def prepare_for_fine_tuning(model, base_model):
    base_model.trainable = True
    for layer in base_model.layers[:FREEZE_UNTIL]:
        layer.trainable = False
    trainable_count = sum((1 for l in base_model.layers if l.trainable))
    print(f'[model] Fine-tuning: {trainable_count} base layers unfrozen (first {FREEZE_UNTIL} remain frozen).')
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=LR_PHASE2), loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=['accuracy'])
    model._name = 'WasteClassifier_FineTuned'
    return model