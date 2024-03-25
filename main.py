import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import scipy as sp
from scipy.io import wavfile
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.widgets import CheckButtons

import sounddevice as sd
from stoppable_thread import StoppableThread


class MusicPlayer:
    filename: str
    samplerate: int

    audio: np.ndarray = None
    proccessed_audio: np.ndarray = None

    stream = None
    stream_thread = None

    def __init__(self, window):
        self.__init_gui(window)
        return

    def __init_gui(self, window):
        window.geometry('800x600')
        window.title('Simple Audio Player')

        self.track = tk.StringVar()
        self.status = tk.StringVar()

        trackframe = tk.LabelFrame(window, text="Track playing:")

        # Creating Audio Frame
        buttonframe = tk.LabelFrame(window, text="Original Control Panel")
        buttonframe.pack(fill=tk.X)
        tk.Button(buttonframe, text="PLAY", command=lambda: self.play_song(self.audio)).grid(row=0, column=0)
        tk.Button(buttonframe, text="STOP", command=self.stop_song).grid(row=0, column=1)
        tk.Button(buttonframe, text="SHOW WAVEFORM", command=self.plot_waveform).grid(row=0, column=2)

        # Create Proccess Frame
        proccessframe = tk.LabelFrame(window, text="Proccess Control Panel")
        proccessframe.pack(fill=tk.X)
        tk.Button(proccessframe, text="PROCCESS", command=self.proccess_song).grid(row=0, column=0)

        # Create Proccessed Audio Frame
        proccessedframe = tk.LabelFrame(window, text="Proccessed Audio Control Panel")
        proccessedframe.pack(fill=tk.X)
        tk.Button(proccessedframe, text="PLAY", command=lambda: self.play_song(self.proccessed_audio)).grid(row=0, column=0)
        tk.Button(proccessedframe, text="STOP", command=self.stop_song).grid(row=0, column=1)
        tk.Button(proccessedframe, text="SHOW WAVEFORM", command=self.plot_waveform).grid(row=0, column=2)
        
        # Creating Menu Bar
        menubar = tk.Menu(window)
        window.config(menu=menubar)

        # Creating File Menu
        submenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=submenu)
        submenu.add_command(label="Open", command=self.browse_file)
        submenu.add_command(label="Save", command=self.browse_file)
        submenu.add_command(label="Exit", command=window.destroy)
        return

    def plot_waveform(self):
        """
        Function to show the plot of audio data in waveform representation.
        """
        
        channels = self.audio.shape[1]
        length = self.audio.shape[0] / self.samplerate

        # For Stereo Audio
        if channels == 2:
            time = np.linspace(0., length, self.audio.shape[0])
            fig, ax = plt.subplots()
            l0, = ax.plot(time, self.audio[:, 0], label="Left Channel")
            l1, = ax.plot(time, self.audio[:, 1], label="Right Channel")

            plt.legend()
            plt.xlabel("Time [s]")
            plt.ylabel("Amplitude")

            rax = plt.axes([0.05, 0.4, 0.1, 0.15])
            labels = ['Left Channel', 'Right Channel']
            visibility = [True, True]
            check = CheckButtons(rax, labels, visibility)

            def change_visibility(label):
                """
                Function to change the visibility of a said plot's label.
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

    def browse_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("Audio File", "*.wav")])
        self.track.set(self.filename)
        self.samplerate, self.audio = wavfile.read(self.filename)
        self.stream = sd.Stream(samplerate=self.samplerate, channels=self.audio.shape[1])
        return

    def save_file(self):
        proccessed_filename = filedialog.asksaveasfile()
        wavfile.write(proccessed_filename, self.samplerate, self.proccessed_audio)
        return

    def play_song(self, song: np.ndarray):
        if song is not None and self.stream is not None:
            if self.stream.active is True:
                self.stop_song()

            self.stream.start()
            self.stream_thread = StoppableThread(target=self.stream.write, args=(song,))
            self.stream_thread.start()

        return

    def stop_song(self):
        if self.stream is not None and self.stream.active is True:
            self.stream.stop()
            self.stream_thread.stop()

        return

    def proccess_song(self):
        """
        """
        
        def process_channel(data):
            """
            
            """

            wiener_n = 10

            R = np.correlate(data, data, mode='full')
            R = R[(R.size // 2 - wiener_n // 2):(R.size // 2 + wiener_n // 2 + 1)]
            R_matrix = np.array([R[i:(i + wiener_n)] for i in range(wiener_n)])

            P = sp.signal.correlate(data, data, mode='full')
            P = P[P.size//2:P.size//2+wiener_n]

            h = np.linalg.solve(R_matrix, P)

            return sp.signal.lfilter(h, 1.0, data)

        samplerate, data = wavfile.read(self.filename)
        channels = data.shape[1]
        filtered_data = None

        # For Stereo Audio
        if channels == 2:
            data_t = np.transpose(data)
            data_1 = data_t[0]
            data_2 = data_t[1]
            filtered_data_1 = process_channel(data_1)
            filtered_data_2 = process_channel(data_2)
            self.proccessed_audio = np.transpose([filtered_data_1, filtered_data_2])

        # For Mono Audio
        else:
            pass

        
        return filtered_data
    
if __name__ == "__main__":
    try:
        root = tk.Tk()
        MusicPlayer(root)
        root.mainloop()

    except Exception as e:
        messagebox.showerror("Error", e)
        exit(code=1)
