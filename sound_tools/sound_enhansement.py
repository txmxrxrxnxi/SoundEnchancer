"""
This is the sound_enhansement module. It provides SoundEnchansement class
to work with different audio enhansement methods.
"""


import numpy as np
import scipy as sp
from scipy import signal


class SoundEnhansement:
    """
    Class that contains different sound enhansement methods.
    """

    def audio_decorator(process_channel):
        def wrapper(samplerate: int, data: np.ndarray):
            channels = data.shape[1]
            filtered_data = None

            # For Stereo Audio
            if channels == 2:
                filtered_data = np.transpose([process_channel(samplerate, ch) for ch in np.transpose(data)])

            # For Mono Audio
            else:
                filtered_data = process_channel(samplerate, data)

            return filtered_data
        return wrapper

    @staticmethod
    @audio_decorator
    def wiener(samplerate: int, data: np.ndarray):
        def wiener_filter(psd, noise_pds, N):
            H = psd / (psd + noise_pds)
            taps = np.fft.irfft(H, n=N)
            return taps

        def get_noise_psd(psd, fs, N):
            i = np.arange(N)
            coef = 2 * np.pi * fs * i / N
            psd_noise_1 = np.array(np.sum(psd * np.sin(coef)))
            psd_noise_2 = np.array(np.sum(psd * np.cos(coef)))
            psd_noise = np.abs(psd_noise_1 - psd_noise_2) ** 1.5
            return psd_noise

        normalized = data / np.max(np.abs(data))
        fs, psd = signal.welch(normalized, fs=samplerate)

        N = len(psd)
        psd_noise = get_noise_psd(psd, fs, N)
        taps = wiener_filter(psd, psd_noise, N)

        filtered_audio_data = np.convolve(normalized, taps)
        return filtered_audio_data[:len(data)]

    @staticmethod
    @audio_decorator
    def lib_wiener(samplerate, data: np.ndarray):
        """
        Applies the Wiener filter to the given data.

        Args:
            data (np.ndarray): The input data to be filtered.

        Returns:
            np.ndarray: The filtered data.
        """

        wiener_n = 1024

        R = np.correlate(data, data, mode='full')
        R = R[R.size//2 - wiener_n + 1:R.size//2 + wiener_n]
        R_matrix = np.array([R[i:i+wiener_n] for i in range(wiener_n)])
        P = sp.signal.correlate(data, data, mode='full')
        P = P[P.size//2:P.size//2+wiener_n]

        h, _, _, _ = np.linalg.lstsq(R_matrix, P, rcond=None)

        return signal.lfilter(h, 1.0, data)

if __name__ == "__main__":
    import time
    from scipy.io import wavfile
    samplerate, data = wavfile.read("data\\noise\\clip.wav")

    start_time = time.time()
    res = SoundEnhansement.wiener(samplerate, data)
    end_time = time.time()
    execution_time = end_time - start_time

    wavfile.write("data\\clean\\clip_8.wav", samplerate, res)
    print(f"The process method took {execution_time} seconds to execute.")
