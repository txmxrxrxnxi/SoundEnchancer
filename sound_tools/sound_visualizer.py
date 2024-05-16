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
            l0, = ax.plot(time, audio[:, 0], label="Left Channel")
            l1, = ax.plot(time, audio[:, 1], label="Right Channel")

            plt.legend()
            plt.xlabel("Time [s]")
            plt.ylabel("Amplitude")

            rax = plt.axes([0.05, 0.4, 0.1, 0.15])
            labels = ['Left Channel', 'Right Channel']
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
            raise NotImplementedError()
        
        plt.show()
        return
    