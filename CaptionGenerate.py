from pathlib import Path
import argparse
import whisper
from whisper.utils import get_writer
import os

def GenerateCaptions(file_path, lang):
    video_path = Path(file_path)
    base_name, ext = os.path.splitext(os.path.basename(file_path))
    if not os.path.exists(file_path):
        print(f"Error: The specified file '{VIDEO_PATH}' does not exist.")
        sys.exit(1)

    export_transcript_path = video_path.parent / f'{video_path.stem}_gen.srt'
    model = whisper.load_model("turbo")
    print(f'Processing {video_path}')
    result = model.transcribe(str(video_path), language=lang, task="transcribe", condition_on_previous_text=False, verbose=False)
    
    writer = get_writer('srt', str(export_transcript_path.parent))
    writer(result, str(export_transcript_path))
    print(f'Transcription completed and saved to {export_transcript_path}')


audio_path = "./S01E01 - My Senpai Is a Bunny Girl_jpn_Vocals.wav"
GenerateCaptions(audio_path, "Japanese")
# eng = en
# jpn = Japanese
