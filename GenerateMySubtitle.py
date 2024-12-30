import os
import pysrt

def find_match(wavs, number):
    for f in wavs:
        if os.path.basename(f).strip(".wav") == str(number):
            return f
    return str(number) + " - Not found"

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


def generateJSrt(audio_dir, file1, file2):
    """
     file1 = Base Generated sutitles for the audio given
     file2 = Given Subtitle file of objective langauge to turn to
    """
    wav_files = get_all_wav_files(audio_dir)
    newName = os.path.basename(file1)
    newName = newName[0:newName.index("_")] + ".jsrt"
    output_file = os.path.join(os.path.dirname(file1), newName)

    """ Merging the SRT Files now """

    # Read both SRT files
    srt1 = pysrt.open(file1, encoding='utf-8')
    srt2 = pysrt.open(file2, encoding='utf-8')

    # Prepare the output
    merged_lines = []

    # Match translations based on timing
    for sub1 in srt1:
        # Combine all matching subtitles from the second file
        combined_text = []
        for sub2 in srt2:
            # Check if the subtitle overlaps with the first file's subtitle
            if (
                sub2.start.ordinal >= sub1.start.ordinal
                and sub2.start.ordinal <= sub1.end.ordinal
            ) or (
                sub2.end.ordinal >= sub1.start.ordinal
                and sub2.end.ordinal <= sub1.end.ordinal
            ):
                combined_text.append(sub2.text.strip())

        # Use the first file's timestamps and combine text from the second file
        original_text = sub1.text.strip()
        translated_text = " ".join(combined_text) if combined_text else "No translation available"
        filepath = findMatch(wav_files, sub1.index)
        
        # Custom format
        merged_lines.append(
            f"{filepath}\n"
            f"{sub1.start} --> {sub1.end}\n"
            f"Original: {original_text}\n"
            f"Translated: {translated_text}\n\n"
        )

    # Write the merged output to a new file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.writelines(merged_lines)

    print(f"Merged SRT file saved to {output_file}")
