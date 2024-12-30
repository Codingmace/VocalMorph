from pydub import AudioSegment
import os

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
    f = open(input_my_srt, "r")
    lines = f.readlines()
    wavs = get_all_wav_files(output_dir)
    # Initial
    curFileName = findMatch(lines[0], wavs) # Get the file
    curTime = lines[1].split(' --> ')
    startTime = getMiliSecond(datetime.strptime(curTime[0],format))
    endTime = getMiliSecond(datetime.strptime(curTime[1],format))
    audio1 = AudioSegment.silent(duration=startTime) # Audio file of voices
    audio1 = audio1 + AudioSegment.from_file(curFileName)
    # Everything AFter
    ind = 0
    for i in range(1, len(lines)):
        print(" go through the srt file and put together the voices")

    
    instrumental = AudioSegment.from_file(instrument_file)
    combined = instrumental.overlay(audio1)
    combined.export(os.path.basename(input_my_srt).replace(".jsrt", ".wav"), format="wav")
    
