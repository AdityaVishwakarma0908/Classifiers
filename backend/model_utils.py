import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'mnist_model.pkl')

print("Loading model...")
try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

def process_and_predict(pixel_array: list) -> int:
    """
    Takes a list of 784 integers from the frontend and predicts.
    """
    # Convert list directly to a numpy array
    img_array = np.array(pixel_array)
    
    # Reshape for scikit-learn (1 sample, 784 features)
    img_array = img_array.reshape(1, -1)
    
    # Make the prediction
    prediction = model.predict(img_array)
    
    return int(prediction[0])