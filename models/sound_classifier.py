import torch
import torch.nn as nn
import numpy as np
from models.audio_cnn import AdvancedAudioModel
from features.mel_spectrogram import MelSpectrogramGenerator
from data.audio_loader import UrbanSoundLoader

class SoundClassifier:
    def __init__(self, model_path=None, num_classes=10):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = AdvancedAudioModel(num_classes=num_classes)
        self.model.to(self.device)
        
        self.mel_generator = MelSpectrogramGenerator()
        self.audio_loader = UrbanSoundLoader()
        
        if model_path:
            self.load_model(model_path)
        
        self.model.eval()

    def load_model(self, model_path):
        checkpoint = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])

    def predict(self, audio_file):
        audio = self.audio_loader.load_audio_file(audio_file)
        mel_spectrogram = self.mel_generator.generate_mel_spectrogram(audio)
        tensor_input = self.mel_generator.mel_to_tensor(mel_spectrogram).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(tensor_input)
            probabilities = torch.softmax(outputs, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1)
            
        return {
            'class_index': predicted_class.item(),
            'probabilities': probabilities.cpu().numpy()[0],
            'confidence': torch.max(probabilities).item()
        }

    def predict_batch(self, audio_files):
        predictions = []
        for audio_file in audio_files:
            prediction = self.predict(audio_file)
            predictions.append(prediction)
        return predictions