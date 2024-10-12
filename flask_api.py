from flask import Flask, request, jsonify
from PIL import Image
import io, sys, os, time
import base64
import logging
from logging.handlers import RotatingFileHandler
from concurrent_log_handler import ConcurrentRotatingFileHandler, ConcurrentTimedRotatingFileHandler
from Preprocessing import image_preprocessing
from Preprocessing.image_preprocessing import gamma_correction
import cv2

upload_path = 'UPLOAD'
log_path=os.path.join('LOG','app.log')
if not os.path.exists(log_path):
    os.mkdir('LOG')
if not os.path.exists(upload_path):
    os.mkdir('UPLOAD')

#logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
#RotateFilehandler = RotatingFileHandler(log_path, maxBytes=50, backupCount=5)
formatter = logging.Formatter('%(asctime)s[%(name)s][%(funcName)s][%(levelname)s] - %(message)s')

#CocurrentRotateFilehandler = ConcurrentRotatingFileHandler(log_path, maxBytes=50, backupCount=5)
#CocurrentRotateFilehandler.setFormatter(formatter)
CocurrentTimeRotateFileHandler = ConcurrentTimedRotatingFileHandler(log_path,when='m')
CocurrentTimeRotateFileHandler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(CocurrentTimeRotateFileHandler)
#logger.addHandler(CocurrentRotateFilehandler)
#logger.addHandler(RotateFilehandler)

app = Flask(__name__)

@app.route("/")
def hello():
    logger.info('Hello, World!')
    return "Hello, World!"

@app.route("/echo")
def echo():
    return jsonify({'parameter':'test'}),200

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # 在這裡可以對圖片進行處理
        file.save(os.path.join(upload_path, file.filename))
        image = cv2.imread(os.path.join(upload_path, file.filename))
        gamma=0.5
        pre_processed_image = gamma_correction(cv2.imread(os.path.join(upload_path, file.filename)),gamma)
        cv2.imwrite(os.path.join(upload_path, f"preprocessed_gamma_{gamma}_{file.filename}"), pre_processed_image)
        width, height, channel = image.shape

        logger.info(f"Image received size : {width} {height}")
        return jsonify({"message": "Image received", "size": [width, height]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/uploadByBase64', methods=['POST'])
def upload_imageByBase64():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({"error": "No image part in the request"}), 400

    base64_string = data['image']
    try:
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        filename = str(int(time.time()))
        image.save(os.path.join(upload_path, filename + ".jpeg"))

        gamma=0.5
        original_img = cv2.imread(os.path.join(upload_path, filename + ".jpeg"))
        pre_processed_image = gamma_correction(original_img, gamma)
        cv2.imwrite(os.path.join(upload_path, f"preprocessed_gamma_{gamma}_{filename}.jpeg"), pre_processed_image)

        # 在這裡可以對圖片進行處理
        return jsonify({"message": "Image received", "size": [image.width, image.height]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    logger.info('Flask server started')
    app.run(port=5000)
