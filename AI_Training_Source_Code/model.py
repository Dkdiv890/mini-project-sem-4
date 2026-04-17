import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input

IMG_SIZE = (224, 224)
FREEZE_UNTIL = 0
LR_PHASE1 = 0.001
LR_PHASE2 = 5e-05

def build_model(num_classes, augmentation_layer):
    base_model = EfficientNetB0(input_shape=IMG_SIZE + (3,), include_top=False, weights='imagenet')
    base_model.trainable = False
    
    inputs = tf.keras.Input(shape=IMG_SIZE + (3,), name='input_image')
    x = augmentation_layer(inputs)
    x = preprocess_input(x)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation='softmax', name='output')(x)
    
    model = models.Model(inputs, outputs, name='WasteAI_Core')
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=LR_PHASE1), loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=['accuracy'])
    return (model, base_model)

def prepare_for_fine_tuning(model, base_model):
    base_model.trainable = True
    for layer in base_model.layers[:FREEZE_UNTIL]:
        layer.trainable = False
    
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=LR_PHASE2), loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=['accuracy'])
    return model
