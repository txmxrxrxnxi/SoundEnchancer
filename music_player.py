# GUI Imports
import tkinter as tk
from tkinter import filedialog, messagebox
import pygame

# Math Imports
from scipy.io import wavfile
import numpy as np

# Practical Imports
from sound_enhansement import SoundEnhansement
from sound_visualizer import SoundWaveform
from helpers import create_temp_file, delete_temp_file


class MusicPlayer:
    filename: str = ""
    tempfilename: str = ""

    samplerate: int
    audio: np.ndarray = None
    proccessed_audio: np.ndarray = None

    window: tk.Tk

    status: tk.StringVar
    track: tk.StringVar

    def __init__(self, window):
        self.window = window
        self.__init_music_mixer()
        self.__init_gui()
        return

    def __init_music_mixer(self):
        pygame.init()
        pygame.mixer.init()
        return

    def __init_gui(self):
        self.window.geometry('800x600')
        self.window.title('Simple Audio Player')

        self.__init_track_frame()
        self.__init_button_frame()
        self.__init_procces_frame()
        self.__init_proccessed_frame()

        self.__change_buttons_state("disabled")
        self.__init_menubar()
        return

    def __init_menubar(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        submenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=submenu)
        submenu.add_command(label="Open", command=self.__browse_file, accelerator='Ctrl+O')
        submenu.add_command(label="Save", command=self.__save_file, accelerator='Ctrl+S')
        submenu.add_separator()
        submenu.add_command(label="Close", command=self.__close_file, accelerator='Ctrl+W')
        submenu.add_separator()
        submenu.add_command(label="Exit", command=self.__proper_exit, accelerator='Ctrl+Q')

        helpmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About", command=self.__show_about)
        helpmenu.add_command(label="Show help...", command=self.__show_help)

        self.window.bind('<Control-o>', lambda e: self.__browse_file())
        self.window.bind('<Control-s>', lambda e: self.__save_file())
        self.window.bind('<Control-w>', lambda e: self.__close_file())
        self.window.bind('<Control-q>', lambda e: self.__proper_exit())
        self.window.protocol("WM_DELETE_WINDOW", self.__proper_exit)
        return

    def __init_track_frame(self):
        self.track = tk.StringVar()
        self.status = tk.StringVar()

        trackframe = tk.LabelFrame(self.window, text="Track playing:")
        trackframe.pack(fill=tk.X)
        tk.Label(trackframe, textvariable=self.track).grid(row=0, column=0)
        tk.Label(trackframe, textvariable=self.status).grid(row=1, column=0)

        self.track.set("No Track")
        self.status.set("Stopped")
        return

    def __init_button_frame(self):
        button_frame = tk.LabelFrame(self.window, text="Original Control Panel")
        button_frame.pack(fill=tk.X)
        tk.Button(button_frame, 
                  command=lambda: self.__play_song(self.filename), 
                  text="PLAY").grid(row=0, column=0)
        tk.Button(button_frame, 
                  command=self.__stop_song, 
                  text="STOP").grid(row=0, column=1)
        tk.Button(button_frame, 
                  command=lambda: self.__plot_waveform(self.audio, self.samplerate), 
                  text="SHOW WAVEFORM").grid(row=0, column=2)
        return

    def __init_procces_frame(self):
        proccess_frame = tk.LabelFrame(self.window, text="Proccess Control Panel")
        proccess_frame.pack(fill=tk.X)
        tk.Button(proccess_frame, 
                  command=self.__proccess_song, 
                  text="PROCCESS").grid(row=0, column=0)
        return

    def __init_proccessed_frame(self):
        proccessed_frame = tk.LabelFrame(self.window, text="Proccessed Audio Control Panel")
        proccessed_frame.pack(fill=tk.X)
        tk.Button(proccessed_frame, 
                  command=lambda: self.__play_song(self.tempfilename), 
                  text="PLAY").grid(row=0, column=0)
        tk.Button(proccessed_frame, 
                  command=self.__stop_song, 
                  text="STOP").grid(row=0, column=1)
        tk.Button(proccessed_frame, 
                  command=lambda: self.__plot_waveform(self.proccessed_audio, self.samplerate),
                  text="SHOW WAVEFORM").grid(row=0, column=2)
        return

    def __plot_waveform(self, audio, samplerate):
        SoundWaveform.plot_waveform(audio, samplerate)
        return

    def __browse_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("Audio File", "*.wav")])
        if self.filename == "":
            return

        self.tempfilename = create_temp_file(self.filename)
        self.track.set(self.filename)

        self.samplerate, self.audio = wavfile.read(self.filename)

        self.__change_buttons_state("normal")
        return

    def __save_file(self):
        proccessed_filename = filedialog.asksaveasfile()
        if proccessed_filename == "":
            return

        wavfile.write(proccessed_filename, self.samplerate, self.proccessed_audio)
        return
    
    def __close_file(self):
        self.track.set("")
        self.__stop_song()

        self.filename = ""
        delete_temp_file(self.tempfilename)
        self.tempfilename = ""

        self.samplerate = 0
        self.audio = None
        self.proccessed_audio = None

        self.__change_buttons_state("disabled")
        return

    def __play_song(self, song: str):
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        self.status.set("Playing")
        return

    def __stop_song(self):
        pygame.mixer.music.stop()
        self.status.set("Stopped")
        return

    def __pause_song(self):
        pygame.mixer.music.pause()
        self.status.set("Paused")
        return

    def __proccess_song(self):
        self.proccessed_audio = SoundEnhansement.lib_wiener(self.audio)
        wavfile.write(self.tempfilename, self.samplerate, self.proccessed_audio)
        return
    
    def __change_buttons_state(self, state: str):
        if state not in ["disabled", "normal", "active"]:
            raise ValueError(f"Invalid button state choosen: {state}")
        
        def __get_all_buttons(widget: tk.Misc):
            return [child for child in widget.winfo_children() if isinstance(child, tk.Button)] + \
                sum([__get_all_buttons(child) for child in widget.winfo_children()], [])

        buttons = __get_all_buttons(self.window)
        for button in buttons:
            button.config(state=state)

        return
    
    def __show_about(self):
        messagebox.showinfo("About", "Sound Enchancer by Marria Stanovych.")

    def __show_help(self):
        messagebox.showinfo("Help", "TODO...")

    def __proper_exit(self):
        delete_temp_file(self.tempfilename)
        self.window.destroy()
        return
        