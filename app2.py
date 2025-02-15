from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
import base64
import cv2

app = Flask(__name__)

# Load the model
model_path = "C:/Users/Lenovo/Desktop/Driver-Distraction-Detection/Training Notebooks/model/model.h5"
loaded_model_hdf5 = load_model(model_path)
image_size = 256

class_names = {
    0: "Safe Driving", 1: "Texting - Right Hand", 2: "Talking on the Phone - Right",
    3: "Texting - Left Hand", 4: "Talking on the Phone - Left", 5: "Operating the Radio",
    6: "Drinking", 7: "Reaching Behind", 8: "Hair and Makeup", 9: "Talking to Passenger"
}

def process_image(img):
    img = tf.image.resize(img, (image_size, image_size))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        img_bytes = base64.b64decode(request.data.split(b',')[1])
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = tf.convert_to_tensor(img)
        img = process_image(img)

        # Make prediction
        predictions_hdf5 = loaded_model_hdf5.predict(img)
        predicted_class_hdf5 = class_names[np.argmax(predictions_hdf5[0])]

        return jsonify({"prediction": predicted_class_hdf5})

if __name__ == '__main__':
    app.run(debug=True)
