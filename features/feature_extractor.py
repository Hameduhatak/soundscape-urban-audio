import numpy as np
import librosa

class AudioFeatureExtractor:
    def __init__(self, sample_rate=22050, n_fft=2048, hop_length=512):
        self.sample_rate = sample_rate
        self.n_fft = n_fft
        self.hop_length = hop_length

    def extract_all_features(self, audio):
        features = {}
        
        features['mel_spectrogram'] = self._extract_mel_spectrogram(audio)
        features['mfcc'] = self._extract_mfcc(audio)
        features['spectral_centroid'] = self._extract_spectral_centroid(audio)
        features['spectral_rolloff'] = self._extract_spectral_rolloff(audio)
        features['zero_crossing_rate'] = self._extract_zero_crossing_rate(audio)
        features['rms_energy'] = self._extract_rms_energy(audio)
        features['chroma_stft'] = self._extract_chroma_stft(audio)
        
        return features

    def _extract_mel_spectrogram(self, audio):
        return librosa.feature.melspectrogram(
            y=audio, sr=self.sample_rate, n_fft=self.n_fft, hop_length=self.hop_length
        )

    def _extract_mfcc(self, audio, n_mfcc=13):
        return librosa.feature.mfcc(
            y=audio, sr=self.sample_rate, n_mfcc=n_mfcc, n_fft=self.n_fft, hop_length=self.hop_length
        )

    def _extract_spectral_centroid(self, audio):
        return librosa.feature.spectral_centroid(
            y=audio, sr=self.sample_rate, n_fft=self.n_fft, hop_length=self.hop_length
        )

    def _extract_spectral_rolloff(self, audio):
        return librosa.feature.spectral_rolloff(
            y=audio, sr=self.sample_rate, n_fft=self.n_fft, hop_length=self.hop_length
        )

    def _extract_zero_crossing_rate(self, audio):
        return librosa.feature.zero_crossing_rate(audio, frame_length=self.n_fft, hop_length=self.hop_length)

    def _extract_rms_energy(self, audio):
        return librosa.feature.rms(y=audio, frame_length=self.n_fft, hop_length=self.hop_length)

    def _extract_chroma_stft(self, audio):
        return librosa.feature.chroma_stft(y=audio, sr=self.sample_rate, n_fft=self.n_fft, hop_length=self.hop_length)