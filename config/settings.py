import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SAMPLE_RATE = 22050
    DURATION = 4
    HOP_LENGTH = 512
    N_MELS = 128
    N_FFT = 2048
    MODEL_PATH = "trained_models/sound_classifier.pth"
    AUDIO_UPLOAD_FOLDER = "static/uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'm4a'}
    
    URBAN_SOUND_CLASSES = [
        'air_conditioner', 'car_horn', 'children_playing', 'dog_bark',
        'drilling', 'engine_idling', 'gun_shot', 'jackhammer',
        'siren', 'street_music'
    ]
    
    NOISE_THRESHOLDS = {
        'low': 30,
        'medium': 60,
        'high': 80
    }

config = Config()