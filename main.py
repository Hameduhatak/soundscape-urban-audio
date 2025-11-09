from api.app import app
from config.settings import config
import os

if __name__ == '__main__':
    os.makedirs(config.AUDIO_UPLOAD_FOLDER, exist_ok=True)
    os.makedirs('trained_models', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    
    print("Starting SoundScape Urban Audio Analysis System...")
    print(f"Upload folder: {config.AUDIO_UPLOAD_FOLDER}")
    print("Server running on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)