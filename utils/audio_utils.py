import numpy as np
import librosa
import soundfile as sf
from pydub import AudioSegment
import io

class AudioUtils:
    @staticmethod
    def convert_to_wav(audio_data, sample_rate=22050):
        if isinstance(audio_data, str):
            audio, sr = librosa.load(audio_data, sr=sample_rate)
        else:
            audio = audio_data
        
        return audio, sample_rate

    @staticmethod
    def resize_audio(audio, target_length):
        if len(audio) > target_length:
            return audio[:target_length]
        elif len(audio) < target_length:
            padding = target_length - len(audio)
            return np.pad(audio, (0, padding), mode='constant')
        return audio

    @staticmethod
    def normalize_volume(audio, target_dBFS=-20.0):
        audio_segment = AudioSegment(
            audio.tobytes(),
            frame_rate=22050,
            sample_width=audio.dtype.itemsize,
            channels=1
        )
        
        change_in_dBFS = target_dBFS - audio_segment.dBFS
        normalized_audio = audio_segment.apply_gain(change_in_dBFS)
        
        buffer = io.BytesIO()
        normalized_audio.export(buffer, format="wav")
        buffer.seek(0)
        
        normalized_audio_array, sr = sf.read(buffer)
        return normalized_audio_array

    @staticmethod
    def remove_silence(audio, top_db=20):
        intervals = librosa.effects.split(audio, top_db=top_db)
        non_silent_audio = np.concatenate([audio[start:end] for start, end in intervals])
        return non_silent_audio

    @staticmethod
    def extract_audio_segment(audio, start_time, end_time, sample_rate=22050):
        start_sample = int(start_time * sample_rate)
        end_sample = int(end_time * sample_rate)
        return audio[start_sample:end_sample]