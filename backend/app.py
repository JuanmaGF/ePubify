from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
from pdf2image import convert_from_path
import pytesseract

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return "API for PDF to EPUB conversion"

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdfFile' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['pdfFile']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    pdf_path = os.path.join(UPLOAD_FOLDER, 'uploaded_file.pdf')
    file.save(pdf_path)

    if not has_text(pdf_path):
        apply_ocr(pdf_path)

    epub_path = os.path.join(DOWNLOAD_FOLDER, 'converted_file.epub')
    subprocess.run(['ebook-convert', pdf_path, epub_path])

    return jsonify({'fileUrl': f'/downloads/converted_file.epub'})

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

def has_text(pdf_path):
    return False  # Aquí puedes implementar la lógica para verificar si el PDF tiene texto

def apply_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    text = ''
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
