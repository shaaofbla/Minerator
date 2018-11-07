
import os
import re
from modules.midiUtils import chopPrimer



class saver():
    def __init__(self, parent):
        self.configSaver(parent)
        self.porjectName = parent.projectName
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

    def processPathes(self):
        print self.midiFiles
        jobNamesPattern = re.compile(".*GeneratorOut[/](.*)[/].*[/].*.mid")
        newlist = []
        for match in self.midiFiles:
            newlist.append(jobNamesPattern.findall(match)[0])
        print "re Out", set(newlist)
        
    def removePrimerMidiNotes(self):
        self.processed_midi = []
        for midiFile in self.midiFiles:
            midi = chopPrimer(self.primer, midiFile)
            self.processed_midi.append(midi)

    def getTempMidiFiles(self):
        jobdirs = self.getJobDir()
        self.jobNames = jobdirs
        modeldirs = self.getModelDirs(jobdirs)
        self.getMidiFilePath(modeldirs)

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

