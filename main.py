from extractFeatures import extract_streams
from VocalSeperator import vocal_seperator
from CaptionGenerate import GenerateCaptions
from SplitAudio import splitAudio
from speakerSeperation import seperateSpeakers
from GenerateMySubtitle import generateJSrt
from VocalGenerate import voiceClone
from EmotionDetect import emoteDetect
from MergingFile import masterMerger
from TransferEmotion import TransferEmote
from cleanup import remove_srt_wav, add_stream, convert_to_aac, remove_folder
import os

def main(video_input):
    input_folder = "."
    print("Exporting Streams")
    extract_streams(video_input)
    audio_files = [f for f in os.listdir(input_folder) if f.endswith(".wav")]
    selection = 0
    if len(audio_files) == 1:
        print("Found only 1")
    else:
        print("Audio Stream Options")
        for i in range(0, len(audio_files)):
            print(f"{i}. {audio_files[i]}")
        selection = int(input("Input Audio stream want\n"))
    audio_stream = ""
    audio_stream_file = audio_files[selection]
    languageFound = audio_stream_file.split("_")[1].split(".")[0]
    if languageFound == "eng" or languageFound == "en":
        print("Found English, Can't do anything")
        return
    elif languageFound == "jpn":
        print("Found Japanese can do more")
        audio_stream = "Japanese"
    else:
        print("Language isn't supported yet")
        return
    subtitle_files = [f for f in os.listdir(input_folder) if f.endswith(".srt")]
    print("Output Language Options")
    selection = 0
    for i in range(0, len(subtitle_files)):
        print(f"{i}. {subtitle_files[i]}")
    selection = int(input("Input Subtitle stream want\n"))
    subtitle_stream_file = subtitle_files[selection]
    subtitle_stream = ""
    languageFound = subtitle_stream_file.split("_")[1].split(".")[0]
    if languageFound == "eng" or languageFound == "en":
        subtitle_stream = "en"
    else:
        print("Don't know if would work but going to set it equal to the language")
        subtitle_stream = languageFound

    print("Seperating vocals") # May have issue if not ran as admin or on the C drive
    vocal_seperator(audio_stream_file)

    print("Generate Subtitle for Audio")
    input_vocal_file = audio_stream_file.replace(".wav", "_Vocals.wav")
    GenerateCaptions(input_vocal_file , audio_stream)

    print("Split Audio")
    subtitle_file = audio_stream_file.replace(".wav", "_Vocals_gen.srt")
    output_dir = "tmp"
    splitAudio(input_vocal_file, output_dir, subtitle_file)

    # Need to run on current Audio Set
    print("Group Speakers")
    seperateSpeakers(output_dir)

    print("Group Emotions")
    emoteDetect(output_dir)
    
    print("Write New Detailed Srt")
    # Generate Subtitle Here for me to use in the generation
    generateJSrt(output_dir, subtitle_file, subtitle_stream_file)

    print("Voice Cloning Set")
    # Clone the voices using the subtitle and information given
    input_my_srt = video_input.replace(".mkv", ".jsrt")
    voiceClone(input_my_srt, output_dir, subtitle_stream)

    print("Merge Emotions into Audio file")
    # Reading in to merge files and get rid of other
    TransferEmote(input_my_srt, output_dir)
    
    print("Merge to final file")
    # Merging the audio and the instrumental back together
    instrument_file = audio_stream_file.replace(".wav", "_Instruments.wav")
    masterMerger(instrument_file, output_dir, input_my_srt)

    # Cleanup And merge into the file
    print("Cleaning Up Now")
    if os.path.exists(output_dir):
        remove_folder(output_dir)
    wavFile = video_input.replace(".mkv", ".wav")
    newAudio = video_input.replace(".mkv", ".aac")
    convert_to_aac(wavFile)
    outputFile = video_input.replace(".mkv", "_new.mkv")
    add_stream(video_input, outputFile, newAudio)
    remove_srt_wav(".")
    
#input_file = input("Input Starting Video File\n")
input_file = "S01E01 - My Senpai Is a Bunny Girl.mkv"
main(input_file)
