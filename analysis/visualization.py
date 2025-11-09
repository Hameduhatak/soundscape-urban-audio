import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

class SoundVisualizer:
    def __init__(self):
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")

    def plot_waveform(self, audio, sample_rate=22050, title="Audio Waveform"):
        fig = go.Figure()
        
        time = np.linspace(0, len(audio) / sample_rate, num=len(audio))
        
        fig.add_trace(go.Scatter(
            x=time,
            y=audio,
            mode='lines',
            name='Waveform',
            line=dict(color='blue', width=1)
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Time (s)',
            yaxis_title='Amplitude',
            template='plotly_white'
        )
        
        return fig

    def plot_spectrogram(self, mel_spectrogram, title="Mel Spectrogram"):
        fig = go.Figure(data=go.Heatmap(
            z=mel_spectrogram,
            colorscale='Viridis',
            colorbar=dict(title="dB")
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Time',
            yaxis_title='Mel Frequency',
            template='plotly_white'
        )
        
        return fig

    def plot_sound_distribution(self, sound_counts, title="Sound Class Distribution"):
        classes = list(sound_counts.keys())
        counts = list(sound_counts.values())
        
        fig = px.bar(
            x=classes, 
            y=counts,
            title=title,
            labels={'x': 'Sound Classes', 'y': 'Count'},
            color=counts,
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(template='plotly_white')
        return fig

    def plot_noise_analysis(self, noise_data, title="Noise Level Analysis"):
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Decibel Levels', 'Spectral Centroid', 
                          'Zero Crossing Rate', 'Energy Distribution')
        )
        
        if 'decibels' in noise_data:
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=noise_data['decibels'],
                    title={'text': "Decibels"},
                    domain={'row': 0, 'col': 0}
                ),
                row=1, col=1
            )
        
        return fig

    def create_urban_sound_dashboard(self, analysis_results):
        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{"type": "bar"}, {"type": "indicator"}],
                   [{"type": "heatmap"}, {"type": "pie"}]],
            subplot_titles=('Sound Distribution', 'Noise Level', 
                          'Spectrogram', 'Class Probabilities')
        )
        
        return fig