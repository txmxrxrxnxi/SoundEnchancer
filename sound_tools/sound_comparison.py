import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import stft


class SoundComparison:
    @staticmethod
    def compare_audio(data_1: tuple[int, str], data_2: tuple[int, str]):
        sr1, y1 = data_1
        sr2, y2 = data_2

        y1 = y1 / np.max(np.abs(y1))
        y2 = y2 / np.max(np.abs(y2))

        _, _, D1 = stft(y1, sr1)
        _, _, D2 = stft(y2, sr2)

        contrast1 = np.mean(np.abs(D1), axis=0)
        contrast2 = np.mean(np.abs(D2), axis=0)

        clearness1 = np.mean(contrast1)
        clearness2 = np.mean(contrast2)

        clearness_diff = np.abs(clearness1 - clearness2)

        abs_diff = np.sum(np.abs(D1 - D2))

        return (abs_diff, clearness_diff)

    @staticmethod
    def visualize_comparison(data_1: tuple[int, str], data_2: tuple[int, str]):
        sr1, y1 = data_1
        sr2, y2 = data_2

        y1 = y1 / np.max(np.abs(y1))
        y2 = y2 / np.max(np.abs(y2))

        _, _, D1 = stft(y1, sr1)
        _, _, D2 = stft(y2, sr2)

        contrast1 = np.mean(np.abs(D1), axis=0)
        contrast2 = np.mean(np.abs(D2), axis=0)

        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        plt.specgram(contrast1, Fs=sr1)
        plt.colorbar(format='%+2.0f dB')
        plt.title('Spectral contrast of file1')
        plt.subplot(1, 2, 2)
        plt.specgram(contrast2, Fs=sr2)
        plt.colorbar(format='%+2.0f dB')
        plt.title('Spectral contrast of file2')
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    sr1, y1 = wavfile.read('data\\clean\\clip_8.wav')
    sr2, y2 = wavfile.read('data\\clean\\clip_lib.wav')

    abs_diff, clearness_diff = SoundComparison.compare_audio((sr1, y1), (sr2, y2))
    print(f'Absolute difference: {abs_diff}, Clearness difference: {clearness_diff}')
    SoundComparison.visualize_comparison((sr1, y1), (sr2, y2))
