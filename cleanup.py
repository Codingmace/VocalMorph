import shutil
import os
import subprocess
import json

def remove_folder(folder_path):
    """
    Removes the specified folder and all its subfolders.

    Args:
        folder_path (str): The path to the folder to be removed.
    """
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"Folder '{folder_path}' and its contents have been removed.")
        except Exception as e:
            print(f"An error occurred while removing the folder: {e}")
    else:
        print(f"The folder '{folder_path}' does not exist.")

def convert_to_aac(input_file):
    base_name, _ = os.path.splitext(os.path.basename(input_file))
    output_file = base_name + ".aac"
    ffmpeg_cmd_2 = [
        "ffmpeg",
        "-i", input_file,
        output_file,
        "-n" # Don't Override
    ]
    subprocess.run(ffmpeg_cmd_2)

def add_stream(input_file, output_file, additional_stream):
    """
    Adds a new input stream to a video using ffmpeg while copying all existing streams.

    Args:
        input_file (str): Path to the input file.
        output_file (str): Path to the output file.
        additional_stream (str): Path to the additional input stream to be added.
    """
    try:
        cmd_probe = [
            "ffprobe", "-v", "error",
            "-show_entries", "stream=index",
            "-of", "json",
            input_file
        ]
        result = subprocess.run(cmd_probe, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        probe_data = json.loads(result.stdout)

        # Count the number of streams in the original input
        original_stream_count = len(probe_data.get("streams", []))

        # The new stream will have an index equal to the original stream count
        new_stream_index = original_stream_count

        # Construct the ffmpeg command
        cmd = [
            "ffmpeg",
            "-i", input_file,  # Input file
            "-i", additional_stream,  # Additional stream
            "-map", "0",  # Map all streams from the first input
            "-map", "1",  # Map all streams from the second input
            f"-metadata:s:{new_stream_index}", "title=MW Gen Audio",  # Set title for the additional stream
            f"-metadata:s:{new_stream_index}", "language=eng",  # Set language for the additional stream
            "-c", "copy",  # Copy streams without re-encoding
            output_file,  # Output file
            "-y" # Override
        ]
        
        # Execute the ffmpeg command
        subprocess.run(cmd, check=True)
        print(f"Successfully created {output_file} with the additional stream.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running ffmpeg: {e}")

def remove_srt_wav(input_folder):
    wav_files = [f for f in os.listdir(input_folder) if f.endswith(".wav")]
    srt_files = [f for f in os.listdir(input_folder) if f.endswith("srt")]
    for a in wav_files:
        os.remove(a)
    for a in srt_files:
        os.remove(a)

#folder_to_remove = "tmp"
#if os.path.exists(folder_to_remove):
#    remove_folder(folder_to_remove)
#convert_to_aac("S01E01 - My Senpai Is a Bunny Girl.wav")

# Example usage:
#input_video = "S01E01 - My Senpai Is a Bunny Girl.mkv"
#output_video = "S01E01 - My Senpai Pt 2.mkv"
#additional_audio = "S01E01 - My Senpai Is a Bunny Girl.aac"

#add_stream(input_video, output_video, additional_audio)

#input_folder = "."
#remove_srt_wav(input_folder)
