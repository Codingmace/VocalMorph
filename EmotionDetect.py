from speechbrain.inference.interfaces import foreign_class
import os
import shutil
# Needs custom_interface.py

def createFold(path):
    if not os.path.exists(path):
        os.mkdir(path)

def get_all_wav_files(root_folder):
    """
    Traverse a folder and its subfolders to collect all .wav files.

    Args:
        root_folder (str): The path to the root folder.

    Returns:
        list: A list of file paths for all .wav files found.
    """
    wav_files = []

    # Walk through the directory and subdirectories
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith(".wav"):
                wav_files.append(os.path.join(dirpath, filename))

    return wav_files

def emoteDetect(input_dir):
    classifier = foreign_class(source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP", pymodule_file="custom_interface.py", classname="CustomEncoderWav2vec2Classifier")
    wavFiles = get_all_wav_files(input_dir)
    for f in wavFiles:
        try:
            out_prob, score, index, text_lab = classifier.classify_file(f)
            curPath = os.path.join(os.path.dirname(f), text_lab[0])
            createFold(curPath)
            output_file = os.path.join(curPath , os.path.basename(f))
            shutil.move(f , output_file)
        except:
            curPath = os.path.join(os.path.dirname(f), "neu")
            createFold(curPath)
            output_file = os.path.join(curPath , os.path.basename(f))
            shutil.move(f , output_file)

#input_fold = "S01E01_Audio"
#emoteDetect(input_fold)
