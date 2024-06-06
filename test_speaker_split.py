# pip install git+https://github.com/speechbrain/speechbrain.git

import os
import torch
from pyannote.audio import Pipeline
import librosa
import soundfile as sf
import numpy as np

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# import the HF_HUB_TOKEN from the environment
HF_HUB_TOKEN = os.getenv("HF_HUB_TOKEN")

if HF_HUB_TOKEN is None:
    raise ValueError("HF_HUB_TOKEN is not set. Please set the Hugging Face Hub token.")

# Load pre-trained speaker diarization pipeline and move to GPU if available
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=HF_HUB_TOKEN).to(device)


# Path to your audio file
audio_file = "test_pcm.wav"

# Perform speaker diarization
diarization = pipeline(audio_file)

# Load the audio file
audio, sr = librosa.load(audio_file, sr=None)

# Initialize empty arrays for each speaker with the same length as the input audio
speaker_a_audio = np.zeros_like(audio)
speaker_b_audio = np.zeros_like(audio)

# Save segments for each speaker
for segment in diarization.itertracks(yield_label=True):
    start_sample = int(segment[0].start * sr)
    end_sample = int(segment[0].end * sr)
    speaker_label = segment[2]

    # Debugging: print start and end times
    print(f"Speaker {speaker_label}: start_time={segment[0].start}, end_time={segment[0].end}")
    print(f"Speaker {speaker_label}: start_sample={start_sample}, end_sample={end_sample}")

    # Check if segment indices are within bounds
    if start_sample < 0 or end_sample > len(audio):
        print(f"Invalid segment indices for {speaker_label}: start={start_sample}, end={end_sample}")
    else:
        if speaker_label == "SPEAKER_00":
            speaker_a_audio[start_sample:end_sample] += audio[start_sample:end_sample]
        elif speaker_label == "SPEAKER_01":
            speaker_b_audio[start_sample:end_sample] += audio[start_sample:end_sample]

# Debugging: Check the content of speaker arrays
print("Speaker A audio content:", np.any(speaker_a_audio))
print("Speaker B audio content:", np.any(speaker_b_audio))

# Save the audio files for each speaker
sf.write('speaker_a.wav', speaker_a_audio, sr)
sf.write('speaker_b.wav', speaker_b_audio, sr)
