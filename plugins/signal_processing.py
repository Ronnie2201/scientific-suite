"""
Signal processing plugin
"""
import numpy as np
from scipy import signal, fft
import matplotlib.pyplot as plt

class SignalProcessingPlugin:
    """Signal processing tools"""
    
    def __init__(self):
        self.signal = None
        self.sampling_rate = None
        self.time = None
        
    def load_signal(self, data, sampling_rate=1000, time=None):
        """Load signal data"""
        self.signal = np.array(data)
        self.sampling_rate = sampling_rate
        self.dt = 1 / sampling_rate
        
        if time is None:
            self.time = np.arange(len(self.signal)) * self.dt
        else:
            self.time = np.array(time)
        
        return self
    
    def generate_test_signal(self, signal_type='sine', frequency=10, 
                            amplitude=1, duration=1, sampling_rate=1000):
        """Generate test signals"""
        self.sampling_rate = sampling_rate
        self.dt = 1 / sampling_rate
        self.time = np.arange(0, duration, self.dt)
        
        if signal_type == 'sine':
            self.signal = amplitude * np.sin(2 * np.pi * frequency * self.time)
        elif signal_type == 'cosine':
            self.signal = amplitude * np.cos(2 * np.pi * frequency * self.time)
        elif signal_type == 'square':
            self.signal = amplitude * signal.square(2 * np.pi * frequency * self.time)
        elif signal_type == 'sawtooth':
            self.signal = amplitude * signal.sawtooth(2 * np.pi * frequency * self.time)
        elif signal_type == 'chirp':
            self.signal = amplitude * signal.chirp(self.time, 0, duration, frequency)
        elif signal_type == 'gaussian':
            center = duration / 2
            width = duration / 10
            self.signal = amplitude * np.exp(-(self.time - center)**2 / (2 * width**2))
        
        return self
    
    def add_noise(self, noise_level=0.1, noise_type='gaussian'):
        """Add noise to signal"""
        if noise_type == 'gaussian':
            noise = np.random.normal(0, noise_level, len(self.signal))
        elif noise_type == 'uniform':
            noise = np.random.uniform(-noise_level, noise_level, len(self.signal))
        elif noise_type == 'salt_pepper':
            noise = np.zeros_like(self.signal)
            indices = np.random.choice(len(self.signal), 
                                      size=int(noise_level * len(self.signal)), 
                                      replace=False)
            noise[indices] = np.random.choice([-1, 1], size=len(indices)) * np.max(self.signal)
        
        self.signal += noise
        return self
    
    def fourier_transform(self):
        """Compute Fourier transform"""
        n = len(self.signal)
        freq = fft.fftfreq(n, self.dt)
        fft_vals = fft.fft(self.signal)
        
        # Get positive frequencies
        positive_freq = freq[:n//2]
        positive_fft = fft_vals[:n//2]
        
        magnitude = np.abs(positive_fft)
        phase = np.angle(positive_fft)
        power = magnitude**2 / n
        
        return {
            'frequency': positive_freq,
            'magnitude': magnitude,
            'phase': phase,
            'power': power,
            'dominant_freq': positive_freq[np.argmax(magnitude)]
        }
    
    def apply_filter(self, filter_type='lowpass', cutoff=100, order=4):
        """Apply digital filter"""
        nyquist = self.sampling_rate / 2
        normalized_cutoff = cutoff / nyquist
        
        if filter_type == 'lowpass':
            b, a = signal.butter(order, normalized_cutoff, btype='low')
        elif filter_type == 'highpass':
            b, a = signal.butter(order, normalized_cutoff, btype='high')
        elif filter_type == 'bandpass':
            b, a = signal.butter(order, normalized_cutoff, btype='band')
        elif filter_type == 'bandstop':
            b, a = signal.butter(order, normalized_cutoff, btype='stop')
        
        filtered = signal.filtfilt(b, a, self.signal)
        return filtered
    
    def moving_average(self, window_size=10):
        """Apply moving average filter"""
        window = np.ones(window_size) / window_size
        return np.convolve(self.signal, window, mode='same')
    
    def savgol_filter(self, window_size=11, order=2):
        """Apply Savitzky-Golay filter"""
        return signal.savgol_filter(self.signal, window_size, order)
    
    def find_peaks(self, height=None, distance=None):
        """Find peaks in signal"""
        peaks, properties = signal.find_peaks(self.signal, 
                                             height=height, 
                                             distance=distance)
        
        return {
            'indices': peaks,
            'times': self.time[peaks],
            'values': self.signal[peaks],
            'properties': properties
        }
    
    def spectrogram(self, nperseg=256):
        """Compute spectrogram"""
        frequencies, times, Sxx = signal.spectrogram(self.signal, 
                                                     self.sampling_rate,
                                                     nperseg=nperseg)
        
        return {
            'frequencies': frequencies,
            'times': times,
            'spectrogram': 10 * np.log10(Sxx + 1e-10)  # Convert to dB
        }
    
    def autocorrelation(self):
        """Compute autocorrelation"""
        correlation = np.correlate(self.signal, self.signal, mode='full')
        correlation = correlation[len(correlation)//2:]
        correlation = correlation / correlation[0]  # Normalize
        
        lags = np.arange(len(correlation)) * self.dt
        
        return {
            'lags': lags,
            'correlation': correlation,
            'peak_lag': lags[1:][np.argmax(correlation[1:])]  # First peak after zero
        }
    
    def envelope_detection(self):
        """Detect signal envelope using Hilbert transform"""
        analytic_signal = signal.hilbert(self.signal)
        amplitude_envelope = np.abs(analytic_signal)
        instantaneous_phase = np.unwrap(np.angle(analytic_signal))
        instantaneous_frequency = np.diff(instantaneous_phase) / (2.0 * np.pi) * self.sampling_rate
        
        return {
            'envelope': amplitude_envelope,
            'phase': instantaneous_phase,
            'instantaneous_frequency': np.append(instantaneous_frequency, 0)
        }
    
    def plot_signal(self, show_components=False):
        """Plot signal"""
        fig, axes = plt.subplots(2 if show_components else 1, 1, 
                                 figsize=(12, 8 if show_components else 6))
        
        if not show_components:
            ax = axes
            ax.plot(self.time, self.signal, 'b-')
            ax.set_title('Signal')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Amplitude')
            ax.grid(True, alpha=0.3)
        else:
            # Time domain
            axes[0].plot(self.time, self.signal, 'b-')
            axes[0].set_title('Time Domain')
            axes[0].set_xlabel('Time (s)')
            axes[0].set_ylabel('Amplitude')
            axes[0].grid(True, alpha=0.3)
            
            # Frequency domain
            ft = self.fourier_transform()
            axes[1].plot(ft['frequency'], ft['magnitude'], 'r-')
            axes[1].set_title('Frequency Domain')
            axes[1].set_xlabel('Frequency (Hz)')
            axes[1].set_ylabel('Magnitude')
            axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_spectrogram(self):
        """Plot spectrogram"""
        spec = self.spectrogram()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        pcm = ax.pcolormesh(spec['times'], spec['frequencies'], 
                           spec['spectrogram'], shading='gouraud', cmap='viridis')
        ax.set_title('Spectrogram')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Frequency (Hz)')
        plt.colorbar(pcm, ax=ax, label='Power (dB)')
        
        return fig
    
    def signal_statistics(self):
        """Compute signal statistics"""
        stats = {
            'mean': np.mean(self.signal),
            'std': np.std(self.signal),
            'variance': np.var(self.signal),
            'rms': np.sqrt(np.mean(self.signal**2)),
            'peak_to_peak': np.ptp(self.signal),
            'max': np.max(self.signal),
            'min': np.min(self.signal),
            'energy': np.sum(self.signal**2),
            'power': np.mean(self.signal**2)
        }
        
        return stats