import os
import io
import base64
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify, render_template
from PIL import Image

app = Flask(__name__)

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