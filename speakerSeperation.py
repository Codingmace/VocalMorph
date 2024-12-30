from speechbrain.pretrained import SpeakerRecognition
import torchaudio
import os
import shutil

def seperateSpeakers(input_folder):
    # Initialize the pre-trained model
    model = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")

    # Function to check if two audio files are the same speaker
    def are_same_speaker(file1, file2, threshold=0.5):
        """
        Compares two audio files to check if they are from the same speaker.

        Args:
            file1 (str): Path to the first audio file.
            file2 (str): Path to the second audio file.
            threshold (float): Cosine similarity threshold. Higher means stricter match.

        Returns:
            bool: True if same speaker, False otherwise.
            float: Cosine similarity score.
        """
        # Compute the similarity score
        similarity_score = model.verify_files(file1, file2)
        similarity_score = similarity_score[0]
        # Check if the score exceeds the threshold
        is_same_speaker = similarity_score > threshold
        return is_same_speaker, similarity_score

    extra_fold = os.path.join(input_folder, "extra")
    extra_thresh = 5
    if not os.path.exists(extra_fold):
        os.mkdir(extra_fold)
    speaker_ind = 0
    while speaker_ind < 20:
        audio_files = [f for f in os.listdir(input_folder) if f.endswith(".wav")]
        audio_file1 = os.path.join(input_folder , audio_files[0])
        same = []
        diff = []
        for a in audio_files:
            full = os.path.join(input_folder, a)
            # Check if the two files are from the same speaker
            try:
                same_speaker, similarity_score = are_same_speaker(audio_file1, full)
                if same_speaker:
                    same.append(a)
                else:
                    diff.append(a)
            except:
                print(f"Ran into Error")
        print("Same count: ", len(same))
        print("Different Count: ", len(diff))
        print(speaker_ind)
        if len(same) < extra_thresh: # not enough so moving to extra folder
            for a in same:
                shutil.move(os.path.join(input_folder, a), os.path.join(extra_fold, a))
        else:
            speakerName = "Speaker_" + str(speaker_ind)
            speaker_ind = speaker_ind + 1
            newFolder = os.path.join(input_folder, speakerName)
            if os.path.exists(newFolder):
                print("Something fucked up as the folder already exists")
            else:
                os.mkdir(newFolder)
            for a in same:
                shutil.move(os.path.join(input_folder, a), os.path.join(newFolder, a))
        if len(diff) < extra_thresh: # Move remaining before quiting
            for a in diff:
                shutil.move(os.path.join(input_folder, a), os.path.join(extra_fold, a))
            break

# Paths to the audio files
input_folder = "test1"
seperateSpeakers(input_folder)
