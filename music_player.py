# GUI Imports
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pygame

# Math Imports
from scipy.io import wavfile
import numpy as np

# OS imports
from os import path

# Practical Imports
from sound_tools.sound_enhansement import SoundEnhansement
from sound_tools.sound_visualizer import SoundWaveform
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

        self.__init_track_frame()
        self.__init_original_frame()
        self.__init_commands_frame()
        self.__init_proccessed_frame()

        self.__change_buttons_state("disabled")
        self.__init_menubar()
        return

    def __init_menubar(self):
        """
        Initializes the menu bar with File and Help menus.
        """

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

        trackframe = tk.LabelFrame(self.window, text="Track playing:")
        trackframe.pack(fill=tk.X)
        tk.Label(trackframe, textvariable=self.track).grid(row=0, column=0)
        tk.Label(trackframe, textvariable=self.status).grid(row=1, column=0)

        self.track.set("No Track")
        self.status.set("Stopped")
        return

    def __init_original_frame(self):
        """
        Initializes the button frame which contains the PLAY, STOP, and SHOW WAVEFORM 
        buttons for the original audio.
        """

        original_frame = tk.LabelFrame(self.window, text="Original Control Panel")
        original_frame.pack(fill=tk.X)
        tk.Button(original_frame, 
                  command=lambda: self.__play_song(self.filename), 
                  text="PLAY").grid(row=0, column=0)
        tk.Button(original_frame, 
                  command=self.__stop_song, 
                  text="STOP").grid(row=0, column=1)
        tk.Button(original_frame, 
                  command=lambda: self.__plot_waveform(self.audio, self.samplerate), 
                  text="SHOW WAVEFORM").grid(row=0, column=2)
        
        return

    def __init_commands_frame(self):
        """
        Initializes the commands frame which contains the PROCCESS button and 
        a combobox for selecting the processing method.
        """

        commands_frame = tk.LabelFrame(self.window, text="Proccess Control Panel")
        commands_frame.pack(fill=tk.X)
        tk.Button(commands_frame, 
                  command=self.__proccess_song, 
                  text="PROCCESS").grid(row=0, column=0)
        self.proccesing_method = ttk.Combobox(commands_frame,
                     values=["Lib Wiener", "Wiener Filtering"])
        self.proccesing_method.grid(row=0, column=1)

        return

    def __init_proccessed_frame(self):
        """
        Initializes the processed frame which contains the PLAY, STOP, and SHOW WAVEFORM 
        buttons for the processed audio.
        """
        
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
        processing_type = self.proccesing_method.get()

        if processing_type == "Wiener Filtering":
            self.proccessed_audio = SoundEnhansement.wiener(self.samplerate, self.audio)
        else:
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
        