import os
import tensorflow as tf
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.applications.efficientnet import preprocess_input

tf.config.set_visible_devices([], 'GPU')

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')

MODEL_WEIGHTS_PATH = 'best_weights.h5'
CLASS_NAMES = ['metal', 'paper', 'plastic']
IMG_SIZE = (224, 224)

model = None

class FixedDepthwiseConv2D(tf.keras.layers.DepthwiseConv2D):
    def __init__(self, **kwargs):
        if 'groups' in kwargs:
            kwargs.pop('groups')
        super().__init__(**kwargs)

def get_model():
    global model
    if model is None:
        try:
            tf.keras.backend.clear_session()
            from AI_Training_Source_Code.model import build_model, prepare_for_fine_tuning
            from AI_Training_Source_Code.data_loader import get_augmentation_layer
            augmentation = get_augmentation_layer()
            base, _ = build_model(len(CLASS_NAMES), augmentation)
            model = prepare_for_fine_tuning(base, _)
            model.load_weights(MODEL_WEIGHTS_PATH)
            print("Successfully loaded model from best weights!")
        except Exception as e:
            raise e
    return model

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "model_loaded": model is not None}), 200

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        current_model = get_model()
        
        img = Image.open(file.stream).convert('RGB')
        img = img.resize(IMG_SIZE)
        img_array = np.array(img, dtype=np.float32)
        img_array = np.expand_dims(img_array, axis=0)

        predictions = current_model.predict(img_array, verbose=0)
        score = predictions[0]
        
        result = {
            'predictions': {
                CLASS_NAMES[i]: float(score[i]) * 100 for i in range(3)
            },
            'top_class': CLASS_NAMES[int(np.argmax(score))],
            'confidence': round(float(np.max(score)) * 100, 2)
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7860))
    app.run(host='0.0.0.0', port=port, debug=False)
