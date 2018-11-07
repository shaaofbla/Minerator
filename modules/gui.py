import tkinter as tk
from tkinter import simpledialog
import tkSimpleDialog
from mido import MidiFile

from modules.generator import modelNames
from modules.generator import magentaJob
from modules.fileUtils import timeStamp
from modules.saver import saver


class StartPage(tk.Frame):
    def __init__(self, config):
        tk.Frame.__init__(self)
        self.configStartPage(config)
        self.configure(bg=self.colorPalette[1])
        self.pack(side="top", fill = "both", expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(column=0, row=0, sticky=(tk.N,tk.W,tk.E,tk.S))

        self.midi = self.loadMidiFile()
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.pack(pady = 50, padx = 50)
        self.models, _ = modelNames(self.modelDir)
        self.config["MODELS"] = self.models
        self.dropDownStatus = "all"

        self.putMidiButton()
        self.putDropDownLabel()
        self.putModelSelect()
        self.outFileSpinbox = self.putOutFileSpinbox()
        self.putOutFileSpinboxLabel()
        self.outClipLengthSpinbox = self.putOutClipLengthSpinbox()
        self.putOutClipLengthSpinboxLabel()
        self.putRunButton()
        self.saveButton = self.putSaveButton()

    def configStartPage(self, config):
        self.config = config
        self.modelDir = config["MODEL_DIR"]
        self.colorPalette = config["COLOR_PALETTE"]
        self.midiFilename = config["DEFAULT_MIDI_FILE"]

    def loadMidiFile(self):
        self.midi = MidiFile(self.midiFilename)

    def putMidiButton(self):
        midiButton = tk.Button(self, text="Midi File", command=lambda: self.askForMidiFile())
        midiButton.configure(highlightbackground = self.colorPalette[1])
        midiButton.grid(row=0, column=1)
        midiButton.pack()


    def putDropDownLabel(self):
        label = tk.Label(self, text="Choose a Model", bg = self.colorPalette[1])
        label.grid(row=3, column=0)
        label.pack()

    def putModelSelect(self):
        self.dropDownSel = tk.StringVar(self)
        self.dropDownSel.set("all")
        self.dropDownSel.trace('w', self.change_dropdown)
        choices = self.models.keys()
        choices = ['all'] + choices

        dropDown = tk.OptionMenu(self, self.dropDownSel, *choices)
        dropDown.configure(background = self.colorPalette[1])
        dropDown.grid(row=4, column=0)
        dropDown.pack()

    def putOutFileSpinbox(self):
        spinbox = tk.Spinbox(self, from_ = 1, to = 100,width = 5)
        spinbox.configure(background = self.colorPalette[3])
        spinbox.grid(row = 4, column = 2,sticky="W")
        spinbox.pack()
        return spinbox

    def putOutFileSpinboxLabel(self):
        label = tk.Label(self, text = "Number of Files Generated", bg = self.colorPalette[1])
        label.grid(row=3,column = 2, sticky = "W")
        label.pack()

    def putOutClipLengthSpinbox(self):
        spinbox = tk.Spinbox(self, from_ = 1,to = 100, width = 5)
        spinbox.configure(background = self.colorPalette[3])
        spinbox.grid(row = 4, column =1, sticky = "W")
        spinbox.pack()
        return spinbox

    def putOutClipLengthSpinboxLabel(self):
        label = tk.Label(self, text = "Midi-Clip Length (Bars)", bg = self.colorPalette[1])
        label.grid(row=3, column = 1, sticky="W")
        label.pack()

    def putRunButton(self):
        runButton = tk.Button(self, text="Run", command=lambda: self.runJob(), highlightbackground = self.colorPalette[4])
        runButton.grid(row=5, column=1)
        runButton.pack()

    def putSaveButton(self):
        button = tk.Button(self, text="Save",
                           #state=tk.DISABLED ,
                           command=lambda: self.save(), highlightbackground = self.colorPalette[2])
        button.grid(row=6, column=1)
        button.pack()
        return button

    #### Call backs ####
    def askForMidiFile(self):
        fileTypes = (("Midi files","*.midi"),("Mid files","*.mid"))
        filename = tk.filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = fileTypes)
        if filename != '':
            self.midiFilename = filename
            self.loadMidiFile()

    def runJob(self):
        job = magentaJob(self)
        job.run()
        self.saveButton.configure(state="normal")

    def change_dropdown(self, *args):
        self.dropDownStatus = self.dropDownSel.get()
        print self.dropDownStatus

    def save(self):
        self.projectName = tkSimpleDialog.askstring(title="Project Name", prompt ="Give your Project a name peace!",initialvalue="Mofo3000-{}".format(timeStamp()))
        self.saveDir = tk.filedialog.askdirectory(initialdir = "./",title = "Select Directory")
        jobSaver = saver(self)
        jobSaver.save()
