import librosa
import numpy as np
from scipy.io import wavfile
import os


def generate_noise(type, length, sr=44100):
    if type == "white":
        noise = np.random.normal(0, sr, length)
    elif type == "pink":
        num_columns = int(np.ceil(np.log2(length)))
        num_rows = length
        array = np.random.randn(num_columns, num_rows)
        noise = np.cumsum(array, axis=1)[:, :length]
        noise = noise[-1] / np.max(np.abs(noise[-1]))
    elif type == "brown":
        white_noise = np.random.normal(0, 1, length)
        noise = np.cumsum(white_noise)
        noise = noise / np.max(np.abs(noise))
    elif type == "random":
        noise = np.random.random(length)
    return noise

def add_noise_to_audio(audio_data, noise):
    return audio_data + noise

mp3_dir = "data/tonoise/"
mp3_files = [f for f in os.listdir(mp3_dir) if f.endswith(".mp3")]
# mp3_files = [f for f in os.listdir(mp3_dir) if f.endswith(".wav")]

for i, mp3_file in enumerate(mp3_files):
    data, samplerate = librosa.load(os.path.join(mp3_dir, mp3_file), sr=None)
    if samplerate != 44100:
        data = librosa.resample(data, orig_sr=samplerate, target_sr=44100)
        samplerate = 44100
    data = data[:(10 * samplerate)]
    wavfile.write(f"data/clean_10/{i}.wav", samplerate, data)
