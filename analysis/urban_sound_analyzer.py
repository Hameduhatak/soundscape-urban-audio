import numpy as np
import json
from models.sound_classifier import SoundClassifier
from analysis.noise_analysis import NoiseAnalyzer
from features.feature_extractor import AudioFeatureExtractor

class UrbanSoundAnalyzer:
    def __init__(self, model_path=None):
        self.classifier = SoundClassifier(model_path)
        self.noise_analyzer = NoiseAnalyzer()
        self.feature_extractor = AudioFeatureExtractor()
        
        self.sound_classes = [
            'air_conditioner', 'car_horn', 'children_playing', 'dog_bark',
            'drilling', 'engine_idling', 'gun_shot', 'jackhammer',
            'siren', 'street_music'
        ]

    def analyze_audio(self, audio_file):
        classification_result = self.classifier.predict(audio_file)
        audio = self.classifier.audio_loader.load_audio_file(audio_file)
        noise_analysis = self.noise_analyzer.comprehensive_analysis(audio)
        features = self.feature_extractor.extract_all_features(audio)
        
        predicted_class = self.sound_classes[classification_result['class_index']]
        
        analysis_result = {
            'filename': audio_file,
            'predicted_class': predicted_class,
            'confidence': float(classification_result['confidence']),
            'noise_analysis': noise_analysis,
            'class_probabilities': {
                self.sound_classes[i]: float(prob) 
                for i, prob in enumerate(classification_result['probabilities'])
            },
            'features_summary': {
                'num_features': len(features),
                'feature_shapes': {k: v.shape for k, v in features.items()}
            }
        }
        
        return analysis_result

    def analyze_urban_area(self, audio_files):
        area_analysis = {
            'total_files': len(audio_files),
            'sound_distribution': {},
            'noise_levels': [],
            'average_decibels': 0,
            'dominant_sounds': []
        }
        
        decibel_sum = 0
        sound_counts = {sound_class: 0 for sound_class in self.sound_classes}
        
        for audio_file in audio_files:
            analysis = self.analyze_audio(audio_file)
            predicted_class = analysis['predicted_class']
            sound_counts[predicted_class] += 1
            decibel_sum += analysis['noise_analysis']['decibels']
            area_analysis['noise_levels'].append(analysis['noise_analysis'])
        
        area_analysis['sound_distribution'] = sound_counts
        area_analysis['average_decibels'] = decibel_sum / len(audio_files) if audio_files else 0
        
        dominant_sounds = sorted(sound_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        area_analysis['dominant_sounds'] = dominant_sounds
        
        return area_analysis

    def generate_urban_report(self, audio_files):
        area_analysis = self.analyze_urban_area(audio_files)
        
        report = {
            'urban_soundscape_report': area_analysis,
            'recommendations': self._generate_recommendations(area_analysis),
            'noise_pollution_index': self._calculate_noise_pollution_index(area_analysis)
        }
        
        return report

    def _generate_recommendations(self, analysis):
        recommendations = []
        avg_db = analysis['average_decibels']
        dominant_sounds = analysis['dominant_sounds']
        
        if avg_db > 70:
            recommendations.append("High noise pollution detected. Consider implementing noise barriers.")
        
        if dominant_sounds[0][0] in ['jackhammer', 'drilling']:
            recommendations.append("Construction noise dominant. Enforce time restrictions for construction work.")
        
        if dominant_sounds[0][0] in ['car_horn', 'engine_idling']:
            recommendations.append("Traffic noise significant. Consider traffic management solutions.")
            
        if len(recommendations) == 0:
            recommendations.append("Sound environment is within acceptable limits.")
            
        return recommendations

    def _calculate_noise_pollution_index(self, analysis):
        avg_db = analysis['average_decibels']
        if avg_db < 50:
            return "Low"
        elif avg_db < 70:
            return "Moderate"
        else:
            return "High"