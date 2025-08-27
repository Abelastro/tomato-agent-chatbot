from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from PIL import Image
import numpy as np
import io
import os
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Union, Optional, Any

# Add shared directory to path for disease mapping
sys.path.append(str(Path(__file__).parent.parent))
from shared.disease_mapping import map_cnn_to_kb, get_human_readable_name

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model', 'mainModel.keras')
IMAGE_SIZE: Tuple[int, int] = (224, 224)
CLASS_NAMES: List[str] = [
    'Tomato_Bacterial_spot',
    'Tomato_Early_blight',
    'Tomato_Late_blight',
    'Tomato_Leaf_Mold',
    'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two-spotted_spider_mite',
    'Tomato_Target_Spot',
    'Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato_mosaic_virus',
    'Tomato_healthy',
    'Tomato_Leaf_Curl_Virus'
]

model: Optional[Any] = None
try:
    if os.path.exists(MODEL_PATH):
        model = load_model(MODEL_PATH)
        app.logger.info(f"Model loaded from {MODEL_PATH}")
    else:
        app.logger.error(f"Model not found at {MODEL_PATH}")
except Exception as e:
    app.logger.error(f"Error loading model: {e}", exc_info=True)

def preprocess_image(image_bytes: bytes) -> Optional[np.ndarray]:
    # Prepare image for prediction
    try:
        img = Image.open(io.BytesIO(image_bytes))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img = img.resize(IMAGE_SIZE)
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        return img_array
    except Exception as e:
        app.logger.error(f"Preprocessing error: {e}", exc_info=True)
        return None

@app.route('/predict', methods=['POST'])
def predict() -> Tuple[Any, int]:
    if model is None:
        return jsonify({'error': 'Model unavailable.'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'No file in request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            image_bytes = file.read()
            preprocessed_img = preprocess_image(image_bytes)
            if preprocessed_img is None:
                return jsonify({'error': 'Image preprocessing failed'}), 500

            predictions = model.predict(preprocessed_img)
            predicted_class_index = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_index])

            # Check for valid prediction
            if predicted_class_index >= len(CLASS_NAMES):
                app.logger.error(f"Class index {predicted_class_index} out of bounds.")
                return jsonify({'error': 'Invalid class index.'}), 500

            # Confidence threshold for valid leaf detection
            if confidence < 0.7:
                return jsonify({
                    'className': 'No leaf detected',
                    'message': 'Please upload a new photo with all leaf parts.'
                })
            else:
                predicted_class_name = CLASS_NAMES[predicted_class_index]
                kb_slug = map_cnn_to_kb(predicted_class_name)
                human_name = get_human_readable_name(kb_slug) if kb_slug else predicted_class_name

                return jsonify({
                    'className': predicted_class_name,
                    'kbSlug': kb_slug,
                    'humanName': human_name,
                    'confidence': round(confidence * 100, 2)
                })

        except Exception as e:
            app.logger.error(f"Prediction error: {e}", exc_info=True)
            return jsonify({'error': f'Prediction error: {str(e)}'}), 500

    return jsonify({'error': 'Unknown error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
