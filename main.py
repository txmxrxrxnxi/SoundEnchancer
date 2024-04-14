from tkinter import Tk, messagebox
from music_player import MusicPlayer


if __name__ == "__main__":
    try:
        root = Tk()
        MusicPlayer(root)
        root.mainloop()

    except Exception as e:
        messagebox.showerror("Error", e)
        exit(code=1)
