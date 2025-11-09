import os
import torch
import librosa
import numpy as np
from pathlib import Path

class UrbanSoundLoader:
    def __init__(self, sample_rate=22050, duration=4):
        self.sample_rate = sample_rate
        self.duration = duration
        self.target_length = sample_rate * duration

    def load_audio_file(self, file_path):
        try:
            audio, sr = librosa.load(file_path, sr=self.sample_rate)
            audio = self._pad_audio(audio)
            return audio
        except Exception as e:
            raise Exception(f"Error loading audio file: {str(e)}")

    def _pad_audio(self, audio):
        if len(audio) > self.target_length:
            audio = audio[:self.target_length]
        elif len(audio) < self.target_length:
            padding = self.target_length - len(audio)
            audio = np.pad(audio, (0, padding), mode='constant')
        return audio

    def batch_load_audio(self, file_paths):
        audios = []
        for file_path in file_paths:
            audio = self.load_audio_file(file_path)
            audios.append(audio)
        return np.array(audios)