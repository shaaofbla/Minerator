
import subprocess as sub
import os
import re
import json
from mido import MidiFile
#from modules.fileManipulator import createModelOutDir


class magentaJob():
    def __init__(self, parent):
        self.configMagentaJob(parent)
        self.modelChoice = parent.dropDownStatus
        self.outClipLength = parent.outClipLengthSpinbox.get()
        self.numOutFiles = parent.outFileSpinbox.get()
        self.heat = parent.heat.get()

    def configMagentaJob(self,parent):
        self.tempGeneratorDir = parent.config["TEMPDIR"]
        self.melodyGeneratorPath = parent.config["MELODY_GENERATOR_PATH"]
        self.drumGeneratorPath = parent.config["DRUM_GENERATOR_PATH"]
        self.modelDir = parent.config["MODEL_DIR"]
        self.midiFilename = parent.midiFilename
        self.outDir = parent.config["OUT_DIR"]
        self.midi = MidiFile(self.midiFilename)
        self.models = parent.config["MODELS"]

    def run(self):
        self.generateBaseCommand()
        self.joinBaseArgs()
        self.callMagentaScript()
    
        
    def generateBaseCommand(self):
        melodyCommand = "python " + self.melodyGeneratorPath
        self.melodyBaseCommand = melodyCommand
        drumsCommand = "python " + self.drumGeneratorPath
        self.drumBaseCommand = drumsCommand
        
    def joinBaseArgs(self):
        finalOutClipLength =self.includingInputClipLength()
        args = [ "--primer_midi " + self.midiFilename,
        "--num_outputs={}".format(self.numOutFiles),
        "--num_steps={}".format(finalOutClipLength),
        "--condition_on_primer=true",
        "--inject_primer_during_generation=true",
        "--temperature={}".format(self.heat)]
        self.baseArgs = args
        
    def includingInputClipLength(self):
        length = int((int(self.outClipLength)*4+self.midi.length*2)*4)
        return length
    
    def getAllDrumModels(self):
        models = {}
        for model, attrs in self.models.iteritems():
            if attrs["type"] == "drum":
                models[model] = attrs
        return models
    
    def getAllMelodyModels(self):
        models = {}
        for model, attrs in self.models.iteritems():
            if attrs["type"] == "melody":
                models[model] = attrs
        return models
    
    def callMagentaScript(self):
        if (self.modelChoice == 'all'):
            models = self.models.copy()
        elif (self.modelChoice == 'melodyModelOnly'):
            models = self.getAllMelodyModels()
        elif (self.modelChoice == 'drumsOnly'):
            models = self.getAllDrumModels()
        else:
            models = {self.modelChoice: self.models[self.modelChoice]}

        for model, attributes in models.iteritems():
            model_out = createModelOutDir(self.outDir, model)
            ex_command = self.generateExecCommand(model_out, attributes)
            print ex_command
            sub.call(ex_command, shell=True)
            
    def generateExecCommand(self, model_out, attributes):
        outDir_arg = "--output_dir={}".format(model_out)
        modelPath_arg = "--bundle_file=" + os.path.join(self.modelDir, attributes["file"])
        ex_args = self.baseArgs
        ex_args.append(outDir_arg)
        ex_args.append(modelPath_arg)
        if attributes["type"] == "melody":
            ex_command = self.melodyBaseCommand + ' ' + ' '.join(ex_args)
        else:
            ex_command = self.drumBaseCommand + ' ' + ' '.join(ex_args)
        return ex_command

