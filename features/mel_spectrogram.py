import numpy as np
import librosa
import torch

class MelSpectrogramGenerator:
    def __init__(self, sample_rate=22050, n_mels=128, n_fft=2048, hop_length=512):
        self.sample_rate = sample_rate
        self.n_mels = n_mels
        self.n_fft = n_fft
        self.hop_length = hop_length

    def generate_mel_spectrogram(self, audio):
        mel_spec = librosa.feature.melspectrogram(
            y=audio,
            sr=self.sample_rate,
            n_mels=self.n_mels,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )
        log_mel_spec = librosa.power_to_db(mel_spec, ref=np.max)
        return log_mel_spec

    def mel_to_tensor(self, mel_spectrogram):
        tensor = torch.FloatTensor(mel_spectrogram).unsqueeze(0)
        return tensor

    def generate_batch_spectrograms(self, audios):
        spectrograms = []
        for audio in audios:
            mel_spec = self.generate_mel_spectrogram(audio)
            spectrograms.append(mel_spec)
        return np.array(spectrograms)