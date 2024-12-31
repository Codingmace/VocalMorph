import os

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

def TransferEmote(input_srt, input_dir):
    wavs = get_all_wav_files(input_dir)
    print(len(wavs))
    for i in wavs:
        if os.path.exists(i):
            if "_tmp" in i:
                originalFile = i.replace("_tmp", "")
                print(originalFile, i)
                if os.path.exists(originalFile):
                    os.remove(originalFile)
                os.rename(i, originalFile)


#sr = "S01E01 - My Senpai Is a Bunny Girl.jsrt"
#TransferEmote(sr, "tmp")
