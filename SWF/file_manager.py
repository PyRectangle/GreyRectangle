from tkinter import *
from tkinter import filedialog


def select_file(file_types=[('all files', '*')]):
    Tk().withdraw()
    try:
        return filedialog.askopenfile(filetypes=file_types).name
    except AttributeError:
        return None


def select_folder():
    Tk().withdraw()
    return filedialog.askdirectory()
