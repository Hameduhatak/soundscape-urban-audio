import os
import json
import pickle
import numpy as np
from datetime import datetime

class FileUtils:
    @staticmethod
    def ensure_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def save_analysis_result(result, filename=None):
        FileUtils.ensure_directory('results')
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"results/analysis_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2)
        
        return filename

    @staticmethod
    def load_analysis_result(filename):
        with open(filename, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_model_artifacts(model, history, filename):
        FileUtils.ensure_directory('trained_models')
        
        artifacts = {
            'model_state': model.state_dict(),
            'training_history': history,
            'timestamp': datetime.now().isoformat()
        }
        
        torch.save(artifacts, filename)
        return filename

    @staticmethod
    def save_features(features, filename):
        FileUtils.ensure_directory('features_cache')
        
        with open(filename, 'wb') as f:
            pickle.dump(features, f)
        
        return filename

    @staticmethod
    def load_features(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def get_audio_files(directory, extensions=None):
        if extensions is None:
            extensions = {'.wav', '.mp3', '.flac', '.m4a'}
        
        audio_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    audio_files.append(os.path.join(root, file))
        
        return audio_files