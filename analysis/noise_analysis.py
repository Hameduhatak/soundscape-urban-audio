import numpy as np
import librosa
from scipy import stats

class NoiseAnalyzer:
    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate

    def calculate_decibels(self, audio):
        rms = np.sqrt(np.mean(audio**2))
        if rms == 0:
            return -np.inf
        return 20 * np.log10(rms)

    def analyze_noise_level(self, audio):
        db_level = self.calculate_decibels(audio)
        
        if db_level < 30:
            level = 'low'
        elif db_level < 60:
            level = 'medium'
        else:
            level = 'high'
            
        return {
            'decibels': db_level,
            'level': level,
            'rms': np.sqrt(np.mean(audio**2))
        }

    def spectral_analysis(self, audio):
        spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=self.sample_rate)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=self.sample_rate)[0]
        
        return {
            'spectral_centroid_mean': np.mean(spectral_centroids),
            'spectral_centroid_std': np.std(spectral_centroids),
            'spectral_rolloff_mean': np.mean(spectral_rolloff),
            'spectral_rolloff_std': np.std(spectral_rolloff)
        }

    def temporal_analysis(self, audio):
        zero_crossing_rate = librosa.feature.zero_crossing_rate(audio)[0]
        energy = librosa.feature.rms(y=audio)[0]
        
        return {
            'zero_crossing_mean': np.mean(zero_crossing_rate),
            'zero_crossing_std': np.std(zero_crossing_rate),
            'energy_mean': np.mean(energy),
            'energy_std': np.std(energy)
        }

    def comprehensive_analysis(self, audio):
        noise_analysis = self.analyze_noise_level(audio)
        spectral_analysis = self.spectral_analysis(audio)
        temporal_analysis = self.temporal_analysis(audio)
        
        return {
            **noise_analysis,
            **spectral_analysis,
            **temporal_analysis
        }