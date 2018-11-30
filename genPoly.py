
import Tkinter as tk
from mido import MidiFile
import json
import os
import re

from modules.gui import StartPage
from modules.fileManipulator import createOutdir



class Minerator(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.loadConfigs()
        self.setupConfigs()
        self.loadModelMetaData()
        self.geometry(self.config["WINDOW_SIZE"])
        self.title("Toni's Midi Generator")
        self.iconbitmap(r'/Users/janeramba/Documents/python/GUI/Jonathan-Rey-Simpsons-Homer-Simpson-01-Donut.icns')
        self.configure(bg=self.config["COLOR_PALETTE"][2])
        self.frames = {}

        frame = StartPage(self.config)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky = "nsew")
        self.showFrame(StartPage)


    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def loadConfigs(self):
        with open('config.json', 'r') as fd:
            config = json.load(fd)
        self.config = config
    
    def loadModelMetaData(self):
        model_files = os.listdir(self.config["MODEL_DIR"])
        model_files = sorted(model_files, key=unicode.lower)
        with open('data/modelShortNames.json', 'r') as df:
            shortNames = json.load(df)
        models = dict()
        for f in model_files:
            modelName = re.sub(".mag", "", f)
            if f.startswith("Drums"):
                models[modelName] = {
                    "file": f,
                    "type": "drum",
                    "short": shortNames[modelName]
                }
            else:
                models[modelName] = {
                    "file": f,
                    "type": "melody",
                    "short": shortNames[modelName]
                }
        self.config["MODELS"] = models
    
    def setupConfigs(self):
        winsize = "{}x{}".format(self.config["WIDTH"], self.config["HEIGHT"])
        self.config["WINDOW_SIZE"] = winsize
        self.config["OUT_DIR"] = createOutdir(self.config["TEMPDIR"])


def main():
    app = Minerator()
    print "Entering Mainloop"
    app.mainloop()


if __name__ == "__main__":
    main()