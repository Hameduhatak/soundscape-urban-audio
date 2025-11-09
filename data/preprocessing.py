import numpy as np
import librosa
from scipy import signal

class AudioPreprocessor:
    def __init__(self, sample_rate=22050, n_mels=128, n_fft=2048, hop_length=512):
        self.sample_rate = sample_rate
        self.n_mels = n_mels
        self.n_fft = n_fft
        self.hop_length = hop_length

    def compute_mel_spectrogram(self, audio):
        mel_spec = librosa.feature.melspectrogram(
            y=audio,
            sr=self.sample_rate,
            n_mels=self.n_mels,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )
        log_mel_spec = librosa.power_to_db(mel_spec, ref=np.max)
        return log_mel_spec

    def normalize_audio(self, audio):
        return librosa.util.normalize(audio)

    def remove_noise(self, audio, noise_level=0.01):
        return librosa.effects.preemphasis(audio)

    def extract_mfcc(self, audio, n_mfcc=13):
        mfccs = librosa.feature.mfcc(
            y=audio,
            sr=self.sample_rate,
            n_mfcc=n_mfcc,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )
        return mfccs

    def extract_spectral_centroid(self, audio):
        return librosa.feature.spectral_centroid(
            y=audio,
            sr=self.sample_rate,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )

    def extract_rms_energy(self, audio):
        return librosa.feature.rms(
            y=audio,
            frame_length=self.n_fft,
            hop_length=self.hop_length
        )