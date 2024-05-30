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
        
        channels = audio.shape[1]
        length = audio.shape[0] / samplerate

        # For Stereo Audio
        if channels == 2:
            time = np.linspace(0., length, audio.shape[0])
            fig, ax = plt.subplots()
            fig.canvas.manager.set_window_title("Форма хвилі")
            l0, = ax.plot(time, audio[:, 0], label="Лівий канал")
            l1, = ax.plot(time, audio[:, 1], label="Правий канал")

            plt.legend()
            plt.xlabel("Час")
            plt.ylabel("Амплітуда")

            rax = plt.axes([0.05, 0.4, 0.1, 0.15])
            labels = ["Лівий канал", "Правий канал"]
            visibility = [True, True]
            check = CheckButtons(rax, labels, visibility)

            def change_visibility(label: str) -> None:
                """
                Function to change the visibility of a said plot's label.

                Args:
                    label (str): label to be changed.

                Returns:
                    None.
                """
                
                if label == labels[0]:
                    l0.set_visible(not l0.get_visible())
                elif label == labels[1]:
                    l1.set_visible(not l1.get_visible())

                plt.draw()
                return

            check.on_clicked(change_visibility)

        # For Mono Audio
        else:
            time = np.linspace(0., length, audio.shape[0])
            fig, ax = plt.subplots()
            ax.plot(time, audio, label="Моно канал")
            plt.legend()
            plt.xlabel("Час")
            plt.ylabel("Амплітуда")
        
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
            cmap = plt.get_cmap('inferno')
            Pxx, freqs, bins, im = plt.specgram(audio, NFFT=4096, Fs=samplerate, noverlap=2048, cmap=cmap)
            plt.imshow(10 * np.log10(Pxx + 1e-12), aspect='auto', cmap=cmap, origin='lower')
            plt.title(title)
            plt.xlabel('Час')
            plt.ylabel('Частота')
            plt.colorbar(label='dB')

        # Mono audio
        if len(audio.shape) == 1:
            plt.figure(figsize=(10, 4))
            plot_spectrogram(audio, samplerate, 'Спектрограма (Моно)')
        
        # Stereo audio
        else:
            plt.figure(figsize=(10, 8))
            
            plt.subplot(2, 1, 1)
            plot_spectrogram(audio[:, 0], samplerate, 'Спектрограма (Лівий канал)')
            
            plt.subplot(2, 1, 2)
            plot_spectrogram(audio[:, 1], samplerate, 'Спектрограма (Правий канал)')

        plt.show()
        return
    