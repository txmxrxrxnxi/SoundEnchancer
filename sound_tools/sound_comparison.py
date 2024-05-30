"""
This is the sound_comparisont module. It providesSoundComparison class
to work with different audio comparison methods.
"""


import numpy as np
import librosa

from typing import Tuple


class SoundComparison:
    @staticmethod
    def get_spectral_properties(audio_data: np.ndarray) \
        -> Tuple[np.ndarray, float]:
        """
        Calculates and returns the spectral properties of an audio signal.

        Args:
            y (np.ndarray): The audio time series.

        Returns:
            Tuple[np.ndarray, float]: The spectral centroid and the mean spectral flatness.
        """
        
        D = np.abs(librosa.stft(audio_data))
        centroid = librosa.feature.spectral_centroid(S=D)
        snr = librosa.feature.spectral_flatness(y=audio_data)

        return centroid, np.mean(snr)

    @staticmethod
    def compare_audio(file_1: str, file_2: str) \
        -> Tuple[float, float]:
        """
        Compares two audio files based on their spectral properties.

        Args:
            file_1 (str): The path to the first audio file.
            file_2 (str): The path to the second audio file.

        Returns:
            Tuple[float, float]: The percentage difference in spectral centroid and mean spectral flatness.
        """

        y_1, _ = librosa.load(file_1)
        y_2, _ = librosa.load(file_2)
        centroid_1, mean_1 = SoundComparison.get_spectral_properties(y_1)
        centroid_2, mean_2 = SoundComparison.get_spectral_properties(y_2)

        centroid_diff = np.mean(np.nan_to_num(np.abs(centroid_1 - centroid_2) / centroid_1)) * 100
        mean_diff = (np.abs(mean_1 - mean_2) / mean_1 * 100)
        
        return centroid_diff, mean_diff
