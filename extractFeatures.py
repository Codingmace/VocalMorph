import os
import subprocess
import json

def extract_audio_stream(input_file, stream):
    base_name, _ = os.path.splitext(os.path.basename(input_file))
    stream_index = stream["index"]
    codec_name = stream["codec_name"]
    language = stream.get("tags", {}).get("language", "unknown")
    output_file = f"{base_name}_{language}.{codec_name}"

    # Export the audio stream using ffmpeg
    ffmpeg_cmd_1 = [
        "ffmpeg",
        "-i", input_file,
        "-map", f"0:{stream_index}",
        "-c:a", "copy",  # Avoid re-encoding
        output_file,
        "-y" # Override if exists
    ]

    subprocess.run(ffmpeg_cmd_1, check=True)
    print(f"Extracted audio stream to: {output_file}")
    if "wav" not in output_file:
        final_output_file = f"{base_name}_{language}.wav"
        # Export the audio stream using ffmpeg
        ffmpeg_cmd_2 = [
            "ffmpeg",
            "-i", output_file,
            final_output_file,
            "-n" # Don't Override
        ]
        try:
            subprocess.run(ffmpeg_cmd_2)
            print(f"Converted to wav")
            os.remove(output_file)
            print(f"Deleted Old File")
        except subprocess.CalledProcessError as e:
            if not e.stderr == None:
                print(f"Error running command: {e.stderr}")

def extract_subtitle_stream(input_file, stream):
    base_name, _ = os.path.splitext(os.path.basename(input_file))
    stream_index = stream["index"]
    codec_name = stream.get("codec_name", "srt")  # Default to SRT if codec name is unavailable
    language = stream.get("tags", {}).get("language", "unknown")
    output_file = f"{base_name}_{language}.{codec_name}"

    # Export the subtitle stream using ffmpeg
    ffmpeg_1_cmd = [
        "ffmpeg",
        "-i", input_file,
        "-map", f"0:{stream_index}",
        "-c:s", "copy",  # Avoid re-encoding
        output_file,
        "-y" # Override if exists
    ]
    
    subprocess.run(ffmpeg_1_cmd, check=True)
    print(f"Extracted subtitle stream to: {output_file}")
    if "srt" not in output_file:
        final_output_file = f"{base_name}_{language}.srt"

        # Change to srt file
        ffmpeg_2_cmd = [
            "ffmpeg",
            "-i", output_file,
            final_output_file,
            "-y" # No override
        ]
        try:
            subprocess.run(ffmpeg_2_cmd, check=True)
            print(f"Convert Subtitle to srt")
            os.remove(output_file)
            print(f"Removed Old file")
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {e.stderr}")


def extract_streams(input_file):
    # Run ffprobe to get stream info
    ffprobe_cmd = [
        "ffprobe", 
        "-v", "error", 
        "-show_entries", "stream=index:stream_tags=language:stream=codec_name:stream=codec_type", 
        "-of", "json", 
        input_file
    ]

    try:
        result = subprocess.run(ffprobe_cmd, capture_output=True, text=True, check=True)
        streams = json.loads(result.stdout)["streams"]
        # Extract and process audio streams
        for stream in streams:
            if stream.get("codec_type") == "audio":
                extract_audio_stream(input_file, stream)
            if stream.get("codec_type") == "subtitle":
                extract_subtitle_stream(input_file, stream)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e.stderr}")
    except KeyError as e:
        print(f"KeyError: {e}. The file might not contain audio streams.")

# Example usage
input_media_file = "S01E01 - My Senpai Is a Bunny Girl.mkv"
extract_streams(input_media_file)
