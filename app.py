from flask import Flask, request, jsonify, render_template
from PIL import Image
import pytesseract
from difflib import SequenceMatcher
import os
import platform

app = Flask(__name__)

# Configure Tesseract path based on the platform
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
else:
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Default path for Linux installations

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare-images', methods=['POST'])
def compare_images():
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({"error": "Both image files are required!"}), 400

    image1 = request.files['image1']
    image2 = request.files['image2']

    if image1.filename == '' or image2.filename == '':
        return jsonify({"error": "Please upload valid images!"}), 400

    # Save uploaded images
    path1 = os.path.join(app.config['UPLOAD_FOLDER'], image1.filename)
    path2 = os.path.join(app.config['UPLOAD_FOLDER'], image2.filename)
    image1.save(path1)
    image2.save(path2)

    # Extract text using Tesseract
    text1 = extract_text(path1)
    text2 = extract_text(path2)

    # Compare similarity
    similarity = calculate_similarity(text1, text2)

    # Cleanup
    os.remove(path1)
    os.remove(path2)

    return jsonify({"similarity": similarity, "text1": text1, "text2": text2})

def extract_text(image_path):
    """Extract text from an image using Tesseract OCR."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Error: {str(e)}"

def calculate_similarity(text1, text2):
    """Calculate similarity percentage between two texts."""
    return SequenceMatcher(None, text1, text2).ratio() * 100

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
