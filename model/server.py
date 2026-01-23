from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pdf_reader

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Process the PDF using pdf_reader module
        extracted_topics, error = pdf_reader.process_pdf(file_path)
        
        # Clean up successfully processed file (optional, keeping for now for debugging)
        # os.remove(file_path) 
        
        if error:
            return jsonify({'error': error}), 500
        
        return jsonify({'message': 'File processed successfully', 'topics': extracted_topics})

if __name__ == '__main__':
    print("🚀 Server running on http://localhost:5000")
    app.run(debug=True, port=5000)
