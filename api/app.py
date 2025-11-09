from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from analysis.urban_sound_analyzer import UrbanSoundAnalyzer
from config.settings import config

app = Flask(__name__)
app.config.from_object(config)

analyzer = UrbanSoundAnalyzer()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['AUDIO_UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                analysis_result = analyzer.analyze_audio(filepath)
                return render_template('results.html', result=analysis_result)
            except Exception as e:
                return jsonify({'error': str(e)})
    
    return render_template('upload.html')

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['AUDIO_UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            analysis_result = analyzer.analyze_audio(filepath)
            return jsonify(analysis_result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/batch_analyze', methods=['POST'])
def api_batch_analyze():
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    valid_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['AUDIO_UPLOAD_FOLDER'], filename)
            file.save(filepath)
            valid_files.append(filepath)
    
    if not valid_files:
        return jsonify({'error': 'No valid files provided'}), 400
    
    try:
        area_analysis = analyzer.analyze_urban_area(valid_files)
        return jsonify(area_analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/urban_report', methods=['POST'])
def api_urban_report():
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    valid_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['AUDIO_UPLOAD_FOLDER'], filename)
            file.save(filepath)
            valid_files.append(filepath)
    
    if not valid_files:
        return jsonify({'error': 'No valid files provided'}), 400
    
    try:
        urban_report = analyzer.generate_urban_report(valid_files)
        return jsonify(urban_report)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs(app.config['AUDIO_UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)