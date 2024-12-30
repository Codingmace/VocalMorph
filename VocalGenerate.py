import torch
from TTS.api import TTS
import os
import shutil

def voiceClone(input_my_srt, input_dir, lang):
    # Init TTS
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    f = open(input_my_srt, "r")
    lines = f.readlines()
    ind = 0
    curFile = ""
    WantedText = ""
    for f in lines:
        f = f.strip()
        curInd = ind % 2
        if curInd == 0: # File name
            curFile = str(f)
            # parse out from it the emotion and speaker
            baseAudio = "" # Input the file that we are basing off of based on what is in the folder And we are adding the tmp
            ind += 1
        elif curInd == 1: # Text We Want
            if len(f) < 2: # Need to fix if mutiple lines of text, but shouldn't be
                curPath = os.path.join(input_dir, "tmp.wav") # Need to add tmp to the file name given first off as well
                # Run TTS
                tts.tts_to_file(text=WantedText, speaker_wav=baseAudio, language=lang, file_path=curPath)
                # Clear all variables
                WantedText = ""
                curFile = ""
                ind += 1
            else:
                if len(WantedText) > 3:
                    WantedText += "/r" + WantedText
                else:
                    WantedText = WantedText
        
