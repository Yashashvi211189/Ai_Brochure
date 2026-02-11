"""
app.py

Flask web application for the AI-powered brochure generator.
Replaces the CLI interface with a web UI.
"""

import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename

from scraper import scrape_html
from analyzer import analyze_business
from generator import generate_brochures
from image_generator import generate_brochure_background
from image_analyzer import analyze_image
from text_analyzer import analyze_text

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Ensure upload folder exists
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path('output').mkdir(exist_ok=True)
Path('static/images').mkdir(parents=True, exist_ok=True)


@app.route('/')
def index():
    """Main page with upload form."""
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    """Handle multiple input types: HTML file, image, or text/idea."""
    try:
        input_type = request.form.get('input_type', 'html')
        content_blocks = []
        
        if input_type == 'html':
            if 'html_file' not in request.files:
                return jsonify({'error': 'No HTML file uploaded'}), 400
            
            file = request.files['html_file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            # Save and process HTML
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            content_blocks = scrape_html(filepath)
        
        elif input_type == 'image':
            if 'image_file' not in request.files:
                return jsonify({'error': 'No image file uploaded'}), 400
            
            file = request.files['image_file']
            if file.filename == '':
                return jsonify({'error': 'No image selected'}), 400
            
            # Save and process image
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            content_blocks = analyze_image(filepath)
        
        elif input_type == 'text':
            text_input = request.form.get('text_input', '').strip()
            if not text_input:
                return jsonify({'error': 'No text provided'}), 400
            
            # Process text/idea
            content_blocks = analyze_text(text_input)
        
        else:
            return jsonify({'error': f'Unknown input type: {input_type}'}), 400
        
        # Process content blocks into business profile
        profile = analyze_business(content_blocks)
        brochures = generate_brochures(profile)
        
        # Generate background images for each brochure
        image_paths = {}
        for audience in ['customers', 'investors', 'partners']:
            image_path = generate_brochure_background(profile, audience)
            image_paths[audience] = f'/static/images/{os.path.basename(image_path)}'
        
        # Return results
        return jsonify({
            'success': True,
            'profile': profile,
            'brochures': brochures,
            'images': image_paths
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
