# GUI Imports
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pygame
import json

# Math Imports
from scipy.io import wavfile
import numpy as np

# OS imports
import time
from os import path

# Practical Imports
from sound_tools.sound_enhansement import SoundEnhansement
from sound_tools.sound_visualizer import SoundWaveform
from helpers import create_temp_file, delete_temp_file


class MusicPlayer:
    language: str = ""
    filename: str = ""
    tempfilename: str = ""

    samplerate: int
    audio: np.ndarray = None
    proccessed_audio: np.ndarray = None

    window: tk.Tk

    status: tk.StringVar
    track: tk.StringVar
    proccesing_method: ttk.Combobox

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

        self.__load_language()
        self.__init_track_frame()
        self.__init_original_frame()
        self.__init_commands_frame()
        self.__init_proccessed_frame()

        self.__change_buttons_state("disabled")
        self.__init_menubar()
        return

    def __load_language(self):
        """
        Loads language from properties file.
        """
        
        try:
            with open("./properties/properties.json", 'r') as properties:
                language_name = json.load(properties)["language"]
                with open(f"./properties/{language_name}.json", 'r', encoding="utf8") as language_file:
                    self.language = json.load(language_file)
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Properties file not found: {e.filename}")
            self.__proper_exit()
        return


    def __init_menubar(self):
        """
        Initializes the menu bar with File and Help menus.
        """
        
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        submenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.language["file"], menu=submenu)
        submenu.add_command(label=self.language["open"], command=self.__browse_file, accelerator='Ctrl+O')
        submenu.add_command(label=self.language["save"], command=self.__save_file, accelerator='Ctrl+S')
        submenu.add_separator()
        submenu.add_command(label=self.language["close"], command=self.__close_file, accelerator='Ctrl+W')
        submenu.add_separator()
        submenu.add_command(label=self.language["exit"], command=self.__proper_exit, accelerator='Ctrl+Q')

        helpmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.language["help"], menu=helpmenu)
        helpmenu.add_command(label=self.language["about"], command=self.__show_about)
        helpmenu.add_command(label=self.language["show_help"], command=self.__show_help)

        self.window.bind('<Control-o>', lambda _: self.__browse_file())
        self.window.bind('<Control-s>', lambda _: self.__save_file())
        self.window.bind('<Control-w>', lambda _: self.__close_file())
        self.window.bind('<Control-q>', lambda _: self.__proper_exit())
        self.window.protocol("WM_DELETE_WINDOW", self.__proper_exit)
        return

    def __init_track_frame(self):
        """
        Initializes the track frame which displays the current track and its status.
        """

        self.track = tk.StringVar()
        self.status = tk.StringVar()

        trackframe = tk.LabelFrame(self.window, text=self.language["track_playing"])
        trackframe.pack(fill=tk.X)
        tk.Label(trackframe, textvariable=self.track).grid(row=0, column=0)
        tk.Label(trackframe, textvariable=self.status).grid(row=1, column=0)

        self.track.set(self.language["no_track"])
        self.status.set(self.language["stopped"])
        return

    def __init_original_frame(self):
        """
        Initializes the button frame which contains the PLAY, STOP, and SHOW WAVEFORM 
        buttons for the original audio.
        """

        original_frame = tk.LabelFrame(self.window, text=self.language["original_control_panel"])
        original_frame.pack(fill=tk.X)
        tk.Button(original_frame, 
                  command=lambda: self.__play_song(self.filename), 
                  text=self.language["play"]).grid(row=0, column=0)
        tk.Button(original_frame, 
                  command=self.__stop_song, 
                  text=self.language["stop"]).grid(row=0, column=1)
        tk.Button(original_frame, 
                  command=lambda: self.__plot_waveform(self.audio, self.samplerate), 
                  text=self.language["show_waveform"]).grid(row=0, column=2)
        tk.Button(original_frame, 
                  command=lambda: self.__plot_spectrogram(self.audio, self.samplerate), 
                  text=self.language["show_spectrogram"]).grid(row=0, column=3)
        
        return

    def __init_commands_frame(self):
        """
        Initializes the commands frame which contains the PROCCESS button and 
        a combobox for selecting the processing method.
        """

        commands_frame = tk.LabelFrame(self.window, text=self.language["proccess_control_panel"])
        commands_frame.pack(fill=tk.X)
        self.proccesing_method = ttk.Combobox(commands_frame,
                     values=[self.language["lib_wiener"], self.language["wiener_filtering"]])
        self.proccesing_method.set(self.language["wiener_filtering"])
        self.proccesing_method.grid(row=0, column=0)
        tk.Button(commands_frame, 
                  command=self.__proccess_song, 
                  text=self.language["proccess"]).grid(row=0, column=1)

        return

    def __init_proccessed_frame(self):
        """
        Initializes the processed frame which contains the PLAY, STOP, and SHOW WAVEFORM 
        buttons for the processed audio.
        """
        
        proccessed_frame = tk.LabelFrame(self.window, text=self.language["processed_audio_control_panel"])
        proccessed_frame.pack(fill=tk.X)
        tk.Button(proccessed_frame, 
                  command=lambda: self.__play_song(self.tempfilename), 
                  text=self.language["play"]).grid(row=0, column=0)
        tk.Button(proccessed_frame, 
                  command=self.__stop_song, 
                  text=self.language["stop"]).grid(row=0, column=1)
        tk.Button(proccessed_frame, 
                  command=lambda: self.__plot_waveform(self.proccessed_audio, self.samplerate),
                  text=self.language["show_waveform"]).grid(row=0, column=2)
        tk.Button(proccessed_frame, 
                  command=lambda: self.__plot_spectrogram(self.proccessed_audio, self.samplerate), 
                  text=self.language["show_spectrogram"]).grid(row=0, column=3)
        return

    def __plot_waveform(self, audio, samplerate):
        SoundWaveform.plot_waveform(audio, samplerate)
        return
    
    def __plot_spectrogram(self, audio, samplerate):
        SoundWaveform.plot_spectrogram(audio, samplerate)
        return

    def __browse_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("Audio File", "*.wav")])
        if self.filename == "":
            return

        temp_path = path.dirname(path.abspath(__file__))
        self.tempfilename = create_temp_file(temp_path + "\\" + path.basename(self.filename))
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
        self.status.set(self.language["playing"])
        return

    def __stop_song(self):
        pygame.mixer.music.stop()
        self.status.set(self.language["stopped"])
        return

    def __pause_song(self):
        pygame.mixer.music.pause()
        self.status.set(self.language["paused"])
        return

    def __proccess_song(self):
        processing_type = self.proccesing_method.get()

        start_time = time.time()
        if processing_type == self.language["wiener_filtering"]:
            self.proccessed_audio = SoundEnhansement.wiener(self.samplerate, self.audio)
        else:
            self.proccessed_audio = SoundEnhansement.lib_wiener(self.samplerate, self.audio)
        end_time = time.time()
        time_taken = end_time - start_time

        wavfile.write(self.tempfilename, self.samplerate, self.proccessed_audio)
        messagebox.showinfo(self.language["processing_time"], 
            self.language["time_taken"] + str(time_taken))
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
        messagebox.showinfo(self.language["about"], self.language["about_text"])

    def __show_help(self):
        messagebox.showinfo(self.language["help"], "TODO...")

    def __proper_exit(self):
        delete_temp_file(self.tempfilename)
        self.window.destroy()
        return
        