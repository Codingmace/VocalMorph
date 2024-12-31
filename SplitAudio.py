from datetime import datetime
from pydub import AudioSegment
import os

def getMiliSecond(date):
    seconds = date.second + (date.minute * 60) + (date.hour * 360)
    return (date.microsecond / 10000) + (seconds * 1000)

def splitAudio(audio_file, output_dir, subtitleFile):

    f = open(subtitleFile, "r", encoding='cp437')
    lines = f.readlines()
    chunk = []
    times = []
    phrase = []
    ind = 0
    format = "%H:%M:%S,%f"
    curMessage = ""
    os.makedirs(output_dir, exist_ok=True)
    currentChunk = 0
    audio = AudioSegment.from_file(audio_file)
    for r in lines:
        cur = ind % 3
        r = r.strip()
        if cur == 0:
            if r.isdigit():
                chunk.append(r)
                currentChunk = int(r)
            else:
                print("FUCK")
                break
            ind += 1
        elif cur == 1:
            curTime = r.split(' --> ')
            startTime = getMiliSecond(datetime.strptime(curTime[0],format))
            endTime = getMiliSecond(datetime.strptime(curTime[1],format))
            times.append(str(startTime) + " " + str(endTime))
            audio_segment = audio[startTime:endTime]
            segment_filename = os.path.join(output_dir, f"{currentChunk}.wav")
            audio_segment.export(segment_filename, format="wav")
            ind += 1
        elif cur == 2:
            if len(r) < 1:
                phrase.append(curMessage)
                curMessage = ""
                ind += 1
            else:
                if len(curMessage) > 1:
                    curMessage += "\n" + r
                else:
                    curMessage = r


#subtitleFile = "S01E01 - My Senpai Is a Bunny Girl_jpn_Vocals_gen.srt"
#output_dir = "tmp"
#audio_file = "S01E01 - My Senpai Is a Bunny Girl_jpn_Vocals.wav"
#splitAudio(audio_file, output_dir, subtitleFile)
