import os
import tensorflow as tf
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify, render_template
import io
import base64

# Force CPU to save memory on Render Free Tier
tf.config.set_visible_devices([], 'GPU')

app = Flask(__name__)

MODEL_PATH = 'waste_classification_model.h5'
CLASS_NAMES = ['metal', 'paper', 'plastic']
IMG_SIZE = (224, 224)

class FixedDepthwiseConv2D(tf.keras.layers.DepthwiseConv2D):
    def __init__(self, **kwargs):
        # Removing 'groups' which causes issues between newer TF (Mac) and older TF (Render)
        if 'groups' in kwargs:
            kwargs.pop('groups')
        super().__init__(**kwargs)

print('--- SYSTEM LOG: STARTING MODEL LOAD ---')
try:
    # Adding more aliases for DepthwiseConv2D to catch internal Keras mappings
    custom_objects = {
        'DepthwiseConv2D': FixedDepthwiseConv2D,
        'FixedDepthwiseConv2D': FixedDepthwiseConv2D
    }
    model = tf.keras.models.load_model(MODEL_PATH, custom_objects=custom_objects, compile=False)
    print('--- SYSTEM LOG: MODEL LOADED SUCCESSFULLY! ---')
except Exception as e:
    print(f'--- SYSTEM LOG: ERROR LOADING MODEL: {str(e)} ---')
    model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    try:
        image = Image.open(io.BytesIO(file.read())).convert('RGB')
        image_resized = image.resize(IMG_SIZE)
        img_array = tf.keras.utils.img_to_array(image_resized)
        img_array = tf.expand_dims(img_array, 0)
        predictions = model.predict(img_array)
        score = predictions[0]
        result = {
            'predictions': {CLASS_NAMES[i]: round(float(score[i]) * 100, 2) for i in range(len(CLASS_NAMES))},
            'top_class': CLASS_NAMES[int(np.argmax(score))],
            'confidence': round(float(np.max(score)) * 100, 2)
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)