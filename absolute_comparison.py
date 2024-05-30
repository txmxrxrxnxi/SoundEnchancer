import os
import csv
import numpy as np
import librosa
from sound_tools.sound_comparison import SoundComparison


if __name__ == "__main__":
    noised_files = os.listdir("data/clean_10")
    results = []

    for file in noised_files:
        file_path = os.path.join("data/clean_10", file)
        y_1, _ = librosa.load(file_path)
        centroid_1, mean_1 = SoundComparison.get_spectral_properties(y_1)
        centroid_1, mean_1 = np.mean(centroid_1), np.mean(mean_1)

        wiener_denoised = os.path.join("data/wiener_denoised", file)
        y_2, _ = librosa.load(wiener_denoised)
        centroid_2, mean_2 = SoundComparison.get_spectral_properties(y_2)
        centroid_2, mean_2 = np.mean(centroid_2), np.mean(mean_2)

        lib_wiener_denoised = os.path.join("data/lib_wiener_denoised", file)
        y_3, _ = librosa.load(lib_wiener_denoised)
        centroid_3, mean_3 = SoundComparison.get_spectral_properties(y_3)
        centroid_3, mean_3 = np.mean(centroid_3), np.mean(mean_3)

        lib_wiener_denoised = os.path.join("data/noised_10", file)
        y_4, _ = librosa.load(lib_wiener_denoised)
        centroid_4, mean_4 = SoundComparison.get_spectral_properties(y_4)
        centroid_4, mean_4 = np.mean(centroid_4), np.mean(mean_4)

        results.append([file, centroid_1, mean_1, centroid_2, mean_2, centroid_3, mean_3, centroid_4, mean_4])

    with open("absolute_results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["File", "Clear Centroid", "Clear Mean", "Wiener Centroid", "Wiener Mean", "Lib Wiener Centroid", "Lib Wiener Mean", "Noised Centroid", "Noised Mean"])
        writer.writerows(results)
