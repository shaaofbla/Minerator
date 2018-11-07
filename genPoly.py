from tkinter import filedialog, ttk
import tkinter as tk
from mido import MidiFile
#import re
#import time

from modules.gui import StartPage
from modules.generator import modelNames
from modules.fileManipulator import createOutdir


WIDTH = 500
HEIGHT = 300
WINDOW_SIZE = "{}x{}".format(WIDTH, HEIGHT)
MODEL_DIR = "/Users/janeramba/Documents/python/Mag/"
GENERATOR_PATH = "/Users/janeramba/Documents/python/magenta/magenta/models/polyphony_rnn/polyphony_rnn_generate.py"
TEMPDIR = './.TempGeneratorOut/'

config = {
    "WIDTH" : WIDTH,
    "HEIGHT" : HEIGHT,
    "MODEL_DIR" : MODEL_DIR,
    "GENERATOR_PATH" : GENERATOR_PATH,
    "TEMPDIR": TEMPDIR,
    "OUT_DIR": createOutdir(TEMPDIR),
    "DEFAULT_MIDI_FILE" : './melody.mid',
    "COLOR_PALETTE" : ["#96ceb4","#ffeead", "#ff6f69", "#ffcc5c", "#88d8b0"],
    "DEFAULT_OUT_DIR" : "./"
}


class Minerator(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry(WINDOW_SIZE)
        self.title("Toni's Midi Generator")
        self.iconbitmap(r'/Users/janeramba/Documents/python/GUI/Jonathan-Rey-Simpsons-Homer-Simpson-01-Donut.icns')
        self.colorPalette = config["COLOR_PALETTE"]
        self.configure(bg=self.colorPalette[2])
        self.frames = {}

        frame = StartPage(config)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky = "nsew")
        self.showFrame(StartPage)


    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


'''
runFrame = Frame(root, width = WIDTH, height = 50)
runFrame.configure(bg = colorPalette[4])
runFrame.grid(column=0, row=2, sticky=(N,W,E,S))
runFrame.pack(pady = 10, padx = 10)

saveFrame = Frame(root, width = WIDTH, height = 50)
saveFrame.configure(bg = colorPalette[2])
saveFrame.grid(column=0, row=0, sticky=(N,W,E,S))
saveFrame.pack(pady = 10, padx = 10)
'''
def main():
    app = Minerator()
    print "Entering Mainloop"
    app.mainloop()

if __name__ == "__main__":
    main()