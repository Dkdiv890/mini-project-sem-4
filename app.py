import os
import tensorflow as tf
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify, render_template

# Force CPU to save memory on Render Free Tier
tf.config.set_visible_devices([], 'GPU')

app = Flask(__name__)

MODEL_PATH = 'waste_classification_model.h5'
CLASS_NAMES = ['metal', 'paper', 'plastic']
IMG_SIZE = (224, 224)

# Global model variable for lazy loading
model = None

class FixedDepthwiseConv2D(tf.keras.layers.DepthwiseConv2D):
    def __init__(self, **kwargs):
        # Removing 'groups' which causes issues between newer TF (Mac) and older TF (Render)
        if 'groups' in kwargs:
            kwargs.pop('groups')
        super().__init__(**kwargs)

def get_model():
    global model
    if model is None:
        print('--- SYSTEM LOG: STARTING LAZY MODEL LOAD ---')
        try:
            # Clear any previous session leftovers
            tf.keras.backend.clear_session()
            
            # Robust mapping for custom layers
            custom_objects = {
                'DepthwiseConv2D': FixedDepthwiseConv2D,
                'FixedDepthwiseConv2D': FixedDepthwiseConv2D
            }
            
            # Load without compiling to save memory and avoid optimizer issues
            model = tf.keras.models.load_model(
                MODEL_PATH, 
                custom_objects=custom_objects, 
                compile=False
            )
            print('--- SYSTEM LOG: MODEL LOADED SUCCESSFULLY! ---')
        except Exception as e:
            print(f'--- SYSTEM LOG: ERROR LOADING MODEL: {str(e)} ---')
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
        # 1. Ensure model is loaded (Lazy Load)
        current_model = get_model()
        
        # 2. Process Image
        img = Image.open(file.stream).convert('RGB')
        img = img.resize(IMG_SIZE)
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # 3. Predict
        predictions = current_model.predict(img_array, verbose=0)
        score = tf.nn.softmax(predictions[0])
        
        # 4. Format Results
        result = {
            'predictions': {
                CLASS_NAMES[i]: float(score[i]) * 100 for i in range(3)
            },
            'top_class': CLASS_NAMES[int(np.argmax(score))],
            'confidence': round(float(np.max(score)) * 100, 2)
        }
        return jsonify(result)
    except Exception as e:
        print(f"--- PREDICTION ERROR: {str(e)} ---")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Default to 8080 for local and dynamic for Render
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)