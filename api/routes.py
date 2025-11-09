from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename

from analysis.urban_sound_analyzer import UrbanSoundAnalyzer
from config.settings import config

api_bp = Blueprint('api', __name__)
analyzer = UrbanSoundAnalyzer()

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'UrbanSoundAnalyzer'})

@api_bp.route('/analyze/audio', methods=['POST'])
def analyze_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(config.AUDIO_UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            result = analyzer.analyze_audio(filepath)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': f'Analysis failed: {str(e)}'}), 500
    
    return jsonify({'error': 'File type not allowed'}), 400

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS