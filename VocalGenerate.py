import torch
from TTS.api import TTS
import os
import shutil

def voiceClone(input_my_srt, input_dir, lang):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # Init TTS
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    f = open(input_my_srt, "r", encoding="cp437")
    lines = f.readlines()
    ind = 0
    curFile = ""
    WantedText = ""
    translated = False
    for f in lines:
        f = f.strip()
        curInd = ind % 2
        if curInd == 0: # File name
            curFile = str(f)
            # parse out from it the emotion and speaker
            ind += 1
        elif curInd == 1: # Text We Want
            if "Translated" in f:
                translated = True
            if len(f) < 2: # Need to fix if mutiple lines of text, but shouldn't be
                newFileName = os.path.basename(curFile).replace(".wav", "") + "_tmp.wav"
                curPath = os.path.join(os.path.dirname(curFile), newFileName) # Need to add tmp to the file name given first off as well
                # Run TTS
                try:
                    if "No translation available" not in WantedText:
                        tts.tts_to_file(text=WantedText, speaker_wav=curFile, language=lang, file_path=curPath)
                except:
                    print("Something happened")
                # Clear all variables
                WantedText = ""
                curFile = ""
                ind += 1
                translated = False
            elif translated:
                if len(WantedText) > 3:
                    WantedText += "/n" + f
                else:
                    WantedText = f.replace("Translated:", "")
            else:
                pass # Ignore this one for other things

#input_srt = "S01E01 - My Senpai Is a Bunny Girl.jsrt"
#voiceClone(input_srt ,"S01E01_audios" ,"en")
