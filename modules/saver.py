
import os
import re
from shutil import copyfile
from modules.midiUtils import chopPrimer
from modules.fileUtils import createDir



class saver():
    def __init__(self, parent):
        self.configSaver(parent)
        self.projectName = parent.projectName
        self.saveDir = parent.saveDir

    def configSaver(self, parent):
        self.tempDir = parent.config["TEMPDIR"]
        self.primer = parent.midiFilename

    def save(self):
        self.getTempMidiFiles()
        self.removePrimerMidiNotes()
        self.moveMidiToTarget()


    def moveMidiToTarget(self):
        self.processPathes()
        self.copyMidiFiles()
    
    def copyMidiFiles(self):
        #self.createTargedDirs()
        for midi, targed in zip(self.midiFiles, self.targedFile):
            self.createTargedDir(targed)
            copyfile(midi, targed)
    
    def createTargedDir(self, targed):
        midiFilePattern = re.compile("(.*[/]).*.mid")
        targed = midiFilePattern.findall(targed)[0]
        os.makedirs(targed)

    def processPathes(self):
        jobNamesPattern = re.compile(".*GeneratorOut[/](.*)[/].*[/].*.mid")
        newlist = []
        for midiFile in self.midiFiles:
            newlist.append(jobNamesPattern.findall(midiFile)[0])
        uniqueJobnames = list(set(newlist))
        self.uniqueJobnames = uniqueJobnames
        targedFile = []
        for midiFile in self.midiFiles:
            for i, name in enumerate(uniqueJobnames):
                if midiFile.find(name)!= -1:
                    targedFile.append(midiFile.replace(name, "JobNr{}".format(i)))
        for i, targed in enumerate(targedFile):
            targedFile[i] = targed.replace(self.tempDir, "./{}/".format(self.projectName))
        self.targedFile = targedFile
        
    def removePrimerMidiNotes(self):
        self.processed_midi = []
        for midiFile in self.midiFiles:
            midi = chopPrimer(self.primer, midiFile)
            self.processed_midi.append(midi)

    def getTempMidiFiles(self):
        jobdirs = self.getJobDir()
        self.jobNames = jobdirs
        self.modeldirs = self.getModelDirs(jobdirs)
        self.getMidiFilePath(self.modeldirs)

    def getMidiFilePath(self, modelDirs):
        midiFiles = []
        for model in modelDirs:
            for midiFile in os.listdir(model):
                 if midiFile.endswith('.mid'):
                    midiFiles.append(os.path.join(model,midiFile))
        self.midiFiles = midiFiles

    def getModelDirs(self, jobdirs):
        modeldirs = []
        for jobdirPath in jobdirs:
            for model in os.listdir(jobdirPath):
                modeldirs.append(os.path.join(jobdirPath,model))
        return modeldirs

    def getJobDir(self):
        jobDirs =[]
        for jobdir in os.listdir(self.tempDir):
            if not jobdir.startswith('.'):
                jobdirPath = os.path.join(self.tempDir, jobdir)
                jobDirs.append(jobdirPath)
        return jobDirs

