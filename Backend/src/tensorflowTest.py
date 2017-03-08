#! ../ENV/bin/python
import sys
import os
import wave

import tensorflow as tf
import numpy as np


def loadFolder(path):
    songs = []
    for root, dirs, files in os.walk(path):
        for idx, file in enumerate(files):
            if file.endswith(".wav"):
            	waveRead = wave.open(os.path.join(root, file))
            	waveRead.close()

    return songs


loadFolder("../../Data/samples/cycdh/")