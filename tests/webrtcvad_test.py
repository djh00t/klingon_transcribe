import webrtcvad
import numpy as np
import soundfile as sf

# Function to convert audio to PCM format
def convert_audio_to_pcm(audio, sample_rate):
    # Ensure audio is mono
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)
    
    # Convert to 16-bit PCM
    audio = (audio * 32767).astype(np.int16)
    return audio

# Load the audio file
audio_filepath = "test.wav"
audio, sample_rate = sf.read(audio_filepath)
audio = convert_audio_to_pcm(audio, sample_rate)

# Ensure sample rate is valid (must be 8000, 16000, 32000, or 48000 Hz)
assert sample_rate in [8000, 16000, 32000, 48000], "Invalid sample rate"

# Initialize WebRTC VAD
vad = webrtcvad.Vad()
vad.set_mode(3)  # 0: Normal, 3: Aggressive

# Define the frame duration (must be 10, 20, or 30 ms)
frame_duration = 30
frame_length = int(sample_rate * frame_duration / 1000)
assert len(audio) >= frame_length, "Audio length is shorter than frame length"

# Split audio into frames
frames = [audio[i:i + frame_length] for i in range(0, len(audio), frame_length) if len(audio[i:i + frame_length]) == frame_length]

# Perform VAD
speech_segments = []
current_segment = None

for i, frame in enumerate(frames):
    is_speech = vad.is_speech(frame.tobytes(), sample_rate)
    if is_speech:
        if current_segment is None:
            current_segment = [i * frame_duration / 1000, (i + 1) * frame_duration / 1000]
        else:
            current_segment[1] = (i + 1) * frame_duration / 1000
    else:
        if current_segment is not None:
            speech_segments.append(current_segment)
            current_segment = None

if current_segment is not None:
    speech_segments.append(current_segment)

# Print the VAD segments
print("Detected speech segments (in seconds):")
for start, end in speech_segments:
    print(f"Start: {start:.2f}, End: {end:.2f}")