import numpy as np

from matplotlib import pyplot as plt
from matplotlib.widgets import CheckButtons


class SoundWaveform:
    @staticmethod
    def plot_waveform(audio: np.ndarray, samplerate: int):
        """
        Function to show the plot of audio data in waveform representation.

        Args:
            audio (np.ndarray).
            samplerate (int).

        Returns:
            None.
        """
        
        try:
            channels = audio.shape[1]
        except:
            channels = 1
        length = audio.shape[0] / samplerate

        # For Stereo Audio
        if channels == 2:
            time = np.linspace(0., length, audio.shape[0])
            fig, axs = plt.subplots(2, 1, figsize=(10, 8))
            fig.canvas.manager.set_window_title("Форма хвилі")
            
            axs[0].plot(time, audio[:, 0], label="Лівий канал")
            axs[0].legend()
            axs[0].set_xlabel("Час, с")
            axs[0].set_ylabel("Амплітуда, дБ")
            
            axs[1].plot(time, audio[:, 1], color="orange", label="Правий канал")
            axs[1].legend()
            axs[1].set_xlabel("Час, с")
            axs[1].set_ylabel("Амплітуда, дБ")
        
        # For Mono Audio
        else:
            time = np.linspace(0., length, audio.shape[0])
            fig, ax = plt.subplots()
            ax.plot(time, audio, label="Моно канал")
            plt.legend()
            plt.xlabel("Час, с")
            plt.ylabel("Амплітуда, дБ")
        
        plt.show()
        return
    
    @staticmethod
    def plot_spectrogram(audio: np.ndarray, samplerate: int) -> None:
        """
        Function to show the plot of audio data in spectrogram representation.

        Args:
            audio (np.ndarray).
            samplerate (int).

        Returns:
            None.
        """

        
        def plot_spectrogram(audio, samplerate, title):
            cmap = plt.get_cmap("inferno")
            Pxx, freqs, bins, im = plt.specgram(audio, NFFT=4096, Fs=samplerate, noverlap=2048, cmap=cmap)
            plt.imshow(10 * np.log10(Pxx + 1e-12), aspect="auto", cmap=cmap, origin="lower")
            plt.title(title)
            plt.xlabel("Час, c")
            plt.ylabel("Амплітуда, дБ")
            plt.colorbar(label="dB")

        # Mono audio
        if len(audio.shape) == 1:
            plt.figure(num="Спектрограма", figsize=(10, 4))
            plot_spectrogram(audio, samplerate, "Спектрограма (Моно)")
        
        # Stereo audio
        else:
            plt.figure(num="Спектрограма", figsize=(10, 8))
            
            plt.subplot(2, 1, 1)
            plot_spectrogram(audio[:, 0], samplerate, "Спектрограма (Лівий канал)")
            
            plt.subplot(2, 1, 2)
            plot_spectrogram(audio[:, 1], samplerate, "Спектрограма (Правий канал)")

        plt.show()
        return
    