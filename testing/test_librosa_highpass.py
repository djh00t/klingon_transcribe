import librosa
import soundfile as sf

# Load the audio file
y, sr = librosa.load('test_pcm.wav', sr=None)

# Apply a high-pass filter
y_filtered = librosa.effects.preemphasis(y)

# Save the enhanced audio
sf.write('test_librosa_highpass_filtered_test_pcm.wav', y_filtered, sr)

###
### RESULT: Muffled/faint voice much easier to understand.
###