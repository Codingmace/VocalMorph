from pydub import AudioSegment
import os
from datetime import datetime

def find_match(wavs, number):
    for f in wavs:
        if os.path.basename(f).strip(".wav") == os.path.basename(number).strip(".wav"):
            return f
    return str(number) + " - Not found"

def getMiliSecond(date):
    seconds = date.second + (date.minute * 60) + (date.hour * 360)
    return (date.microsecond / 10000) + (seconds * 1000)

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

def mergeAudio(audio_file1, audio_file2, outputPath):
    # Load the audio files
    audio1 = AudioSegment.from_file(audio_file1)
    audio2 = AudioSegment.from_file(audio_file2)

    # Define the offset for the second audio (in milliseconds)
    offset = 5000  # 5 seconds

    # Create a silent audio segment for the offset
    silence = AudioSegment.silent(duration=offset)

    # Add the silence to the beginning of the second audio
    audio2_with_offset = silence + audio2

    # Overlay the two audio files
    combined = audio1.overlay(audio2_with_offset)

    # Export the combined audio
    combined.export(outputPath, format="wav")

def masterMerger(instrument_file, output_dir, input_my_srt):
    format = "%H:%M:%S,%f"
    f = open(input_my_srt, "r", encoding="cp437")
    lines = f.readlines()
    # Start Silence
    startTime = 0
    audio1 = AudioSegment.silent(duration=startTime) # Audio file of voices
    wavs = get_all_wav_files(output_dir)
    curFileName = ""
    lastEnd = "0"
    for i in range(0, len(lines)):
        if ".wav" in lines[i]:
            curFileName = find_match(wavs, lines[i].strip())
        elif "-->" in lines[i]:
            curTime = lines[i].split(' --> ')
            startTime = getMiliSecond(datetime.strptime(curTime[0],format))
            endTime = getMiliSecond(datetime.strptime(curTime[1].strip(),format))
            audio1 = audio1 + (AudioSegment.from_file(curFileName) - 10)
            newDur = int(lastEnd) - int(startTime)
            if newDur > 10: # Padding if it is > 0 of an issue
                audio1 = audio1 + AudioSegment.silent(duration=startTime)
            lastEnd = endTime

    instrumental = AudioSegment.from_file(instrument_file)
    combined = instrumental.overlay(audio1)
    combined.export(os.path.basename(input_my_srt).replace(".jsrt", ".wav"), format="wav")
    print(os.path.basename(input_my_srt).replace(".jsrt", ".wav"))

    
#ins = "S01E01 - My Senpai Is a Bunny Girl_jpn_Instruments.wav"
#output = "S01E01_Audio"
#jsrt = "S01E01 - My Senpai Is a Bunny Girl.jsrt"
#masterMerger(ins, output, jsrt)
