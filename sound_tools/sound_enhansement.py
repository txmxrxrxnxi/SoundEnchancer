"""
This is the sound_enhansement module. It provides SoundEnchansement class
to work with different audio enhansement methods.
"""


# Math imports
import numpy as np
import scipy as sp
from scipy import signal

# Other imports
from typing import Callable, Any


class SoundEnhansement:
    """
    Class that contains different sound enhansement methods.
    """

    def audio_decorator(process_channel: Callable[[int, np.ndarray], np.ndarray]) \
        -> Callable[[int, np.ndarray], np.ndarray]:
        """
        Decorator function for processing audio data.

        This decorator takes a function that processes a single audio channel, and applies it 
        to each channel of a stereo or mono audio data.

        Args:
            process_channel (Callable[[int, np.ndarray], np.ndarray]): A function that takes a samplerate and 
            a numpy array representing an audio channel, and returns a processed numpy array of the same shape.

        Returns:
            Callable[[int, np.ndarray], np.ndarray]: A resulting wrapper function.
        """

        def wrapper(samplerate: int, data: np.ndarray):
            try:
                channels = data.shape[1]
            except IndexError:
                channels = 1
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
        """
        Applies the custom Wiener filter to the given data.

        Args:
            data (np.ndarray): The input data to be filtered.

        Returns:
            np.ndarray: The filtered data.
        """

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
        Applies the SciPy Lib Wiener filter to the given data.

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
