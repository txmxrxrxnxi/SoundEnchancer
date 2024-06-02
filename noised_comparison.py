import os
import csv
import scipy.io.wavfile
from sound_tools.sound_enhansement import SoundEnhansement
from sound_tools.sound_comparison import SoundComparison


if __name__ == "__main__":
    noised_files = os.listdir("data/noised_10")
    results = []

    for file in noised_files:
        file_path = os.path.join("data/noised_10", file)
        # y_wiener = SoundEnhansement.wiener(sr, y)
        # wiener_path = os.path.join("data/wiener_denoised", file)
        # scipy.io.wavfile.write(wiener_path, sr, y_wiener)

        # y_lib_wiener = SoundEnhansement.lib_wiener(sr, y)
        # lib_wiener_path = os.path.join("data/lib_wiener_denoised", file)
        # scipy.io.wavfile.write(lib_wiener_path, sr, y_lib_wiener)

        wiener_path = os.path.join("data/wiener_denoised", file)
        lib_wiener_path = os.path.join("data/lib_wiener_denoised", file)


        centroid_diff_wiener, mean_diff_wiener = SoundComparison.compare_audio(file_path, wiener_path)
        centroid_diff_lib_wiener, mean_diff_lib_wiener = SoundComparison.compare_audio(file_path, lib_wiener_path)
        print(type(centroid_diff_wiener), " ", type(centroid_diff_lib_wiener))
        results.append([file, centroid_diff_wiener, mean_diff_wiener, centroid_diff_lib_wiener, mean_diff_lib_wiener])


    with open("comparison_results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["File", "Centroid Diff Wiener", "Mean Diff Wiener", "Centroid Diff Lib Wiener", "Mean Diff Lib Wiener"])
        writer.writerows(results)
