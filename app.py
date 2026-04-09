import os
import gradio as gr
import tensorflow as tf
import numpy as np
from PIL import Image
MODEL_PATH = 'waste_classification_model.h5'
CLASS_NAMES = ['metal', 'paper', 'plastic']
IMG_SIZE = (224, 224)
print('Loading model...')
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print('Model loaded successfully!')
except Exception as e:
    print(f'Error loading model: {e}')
    model = None

def predict_image(image):
    if model is None:
        return 'Error: Model file not found or failed to load.'
    image = image.resize(IMG_SIZE)
    img_array = tf.keras.utils.img_to_array(image)
    img_array = tf.expand_dims(img_array, 0)
    predictions = model.predict(img_array)
    score = predictions[0]
    confidences = {CLASS_NAMES[i]: float(score[i]) for i in range(len(CLASS_NAMES))}
    return confidences
demo = gr.Interface(fn=predict_image, inputs=gr.Image(type='pil', label='Upload Image Here'), outputs=gr.Label(num_top_classes=3, label='Prediction'), title='♻️ Waste Classification Model', description='Upload an image containing **Metal**, **Paper**, or **Plastic**. The AI model will predict the type of waste.')
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7860))
    demo.launch(server_name='0.0.0.0', server_port=port)