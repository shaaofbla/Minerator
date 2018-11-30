import time
import Tkinter as tk
from mido import MidiFile
import os


def timeStamp():
    ts = time.strftime("%Y-%m-%d_%H%M%S", time.gmtime())
    return ts

def createModelOutDir(outdir, model):
    model_out = '{}/{}'.format(outdir, model)
    createDir(model_out)
    return model_out

def createOutdir(Dir):
    createDir(Dir)
    outdir = '{}/{}/'.format(Dir,timeStamp())
    createDir(outdir)
    return outdir

def createDir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
