
import subprocess as sub
import os
import re
from mido import MidiFile
from modules.fileManipulator import createModelOutDir

def modelNames(Model_dir):
    model_files = os.listdir(Model_dir)
    model = dict()
    drum_model = dict()
    for f in model_files:
        if f.startswith("Drums"):
            drum_model[re.sub(".magDrums-", "", f)] = f
        else:
            model[re.sub(".mag", "", f)] = f
    return model, drum_model

class magentaJob():
    def __init__(self, parent):
        self.configMagentaJob(parent)
        self.modelChoice = parent.dropDownStatus
        self.outClipLength = parent.outClipLengthSpinbox.get()
        self.numOutFiles = parent.outFileSpinbox.get()
        self.heat = parent.heat.get()

    def configMagentaJob(self,parent):
        self.tempGeneratorDir = parent.config["TEMPDIR"]
        self.generatorPath = parent.config["GENERATOR_PATH"]
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
        command = "python " + self.generatorPath
        self.baseCommand = command
        
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
        print self.outClipLength, self.midi.length
        length = int((int(self.outClipLength)*4+self.midi.length*2)*4)
        print length
        return length
        
    def callMagentaScript(self):
        if (self.modelChoice !='all'):
            models = {self.modelChoice: self.models[self.modelChoice]}
        else:
            models = self.models

        for model,path in models.iteritems():
            model_out = createModelOutDir(self.outDir, model)
            print model_out
            ex_command = self.generateExecCommand(model_out, path)
            sub.call(ex_command, shell=True)
            
    def generateExecCommand(self, model_out, path):
        outDir_arg = "--output_dir={}".format(model_out)
        modelPath_arg = "--bundle_file=" + self.modelDir + path
        ex_args = self.baseArgs
        ex_args.append(outDir_arg)
        ex_args.append(modelPath_arg)
        ex_command = self.baseCommand + ' ' + ' '.join(ex_args)
        return ex_command

