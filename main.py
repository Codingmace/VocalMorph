from extractFeatures import extract_streams
from VocalSeperator import vocal_seperator
from CaptionGeneratr import GenerateCaptions
from SplitAudio import splitAudio
from speakerSeperation import seperateSpeakers
from GenerateMySubtitle import generateJSrt
from VocalGenerate import voiceClone
from EmotionDetect import emoteDetect

def main():
    print("Input Video File")
    video_input = "S01E01 - My Senpai Is a Bunny Girl.mkv"
    print("Exporting Streams")
    extract_streams(video_input)
    audio_files = [f for f in os.listdir(input_folder) if f.endswith(".wav")]
    print("Audio Stream Options")
    for f in audio_files:
        print(f)
    print("Input Audio Stream")
    audio_stream = "japeneese"
    audio_stream_file = "S01E01 - My Senpai Is a Bunny Girl_jpn.wav"
    subtitle_files = [f for f in os.listdir(input_folder) if f.endswith(".srt")]
    print("Output Language Options")
    for f in subtitle_files:
        print(f)
    print("Input Subtitle Stream")
    subtitle_stream = "eng"
    subtitle_stream_file = "S01E01 - My Senpai Is a Bunny Girl_eng.srt"

    print("Seperating vocals") # May have issue if not ran as admin or on the C drive
    vocal_seperator(audio_stream_file)

    print("Generate Subtitle for Audio")
    input_vocal_file = "S01E01 - My Senpai Is a Bunny Girl_jpn_Vocals.wav"
    GenerateCaptions(input_vocal_file , "Japanese")

    print("Split Audio")
    subtitle_file = "S01E01 - My Senpai Is a Bunny Girl_jpn_gen.srt"
    output_dir = "S01E01_audios"
    splitAudio(input_vocal_file, output_dir, subtitle_file)

    # Need to run on current Audio Set
    print("Group Speakers")
    seperateSpeakers(output_dir)

    print("Group Emotions")
    emoteDetect(output_dir)
    
    # Need to be tested Everything Below
    print("Write New Detailed Srt")
    # Generate Subtitle Here for me to use in the generation
    generateJSrt(output_dir, subtitle_file, subtitle_stream_file)

    print("Voice Cloning Set")
    # Clone the voices using the subtitle and information given
    intput_my_srt = "S01E01 - My Senpai Is a Bunny Girl.jsrt"
    output_lang = "en"
    voiceClone(input_my_srt, output_dir, output_lang)
    
    print("Merge Emotions into Audio file")
    # Reading in to merge files and get rid of other    
    mergeEmote(input_my_srt, output_dir
    
    print("Merge to final file"_)
    # Merging the audio and the instrumental back together
    instrument_file = "S01E01 - My Senpai Is a Bunny Girl_jpn_Instruments.wav"
    masterMerger(instrument_file, output_dir, input_my_srt)

