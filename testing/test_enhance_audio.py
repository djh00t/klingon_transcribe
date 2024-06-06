import numpy as np
import torch
from demucs import pretrained
from demucs.apply import apply_model
from demucs.audio import AudioFile
from scipy.io.wavfile import write

import logging
from klingon_transcribe.audio_processor import AudioProcessor

# Function to determine the best available device
def get_best_device():
	if torch.cuda.is_available():
		logging.info("Using CUDA")
		return "cuda"
	elif torch.backends.mps.is_available():
		logging.info("Using MPS")
		return "mps"
	else:
		logging.info("Using CPU")
		return "cpu"

def main():
	# Check for MPS availability and fallback to CPU if MPS is not supported by Demucs
	device = get_best_device()
	logging.info(f"demucs - Loaded demucs model into {device}.")

	# Load the pre-trained model
	model = pretrained.get_model('mdx_extra')
	logging.info("Loaded pre-trained model")
	model.eval()
	logging.info("Model set to evaluation mode")

	# Load the test PCM audio file
	logging.info("Loading test PCM audio file")
	# audio_path = 'test_pcm.wav'
	audio_path = 'test_librosa_highpass_filtered_test_pcm.wav'
	f = AudioFile(audio_path)
	waveform = f.read(streams=0, samplerate=model.samplerate, channels=model.audio_channels)

	# Convert to mono if necessary and then to stereo
	if waveform.shape[0] == 1:  # If mono
		waveform = np.tile(waveform, (2, 1))

	waveform = np.expand_dims(waveform, axis=0)  # Add batch dimension

	# Convert waveform to PyTorch tensor
	waveform_tensor = torch.tensor(waveform, dtype=torch.float32)

	# Apply the model to the audio
	logging.info("Applying model to audio")
	with torch.no_grad():
		sources = apply_model(model, waveform_tensor, device=device, split=True, overlap=0.25)[0]

	# Retrieve the vocals stem (assuming vocals are the first stem in the model output)
	logging.info("Extracting vocals stem")
	vocals = sources[3].cpu().numpy()

	# Normalize vocals to the range [-1, 1]
	logging.info("Normalizing vocals")
	vocals = vocals / np.max(np.abs(vocals))

	# Convert to PCM 16-bit format
	logging.info("Converting vocals to PCM 16-bit format")
	vocals_pcm16 = (vocals * 32767).astype(np.int16)

	# Ensure the vocals array is 2D (channels, samples)
	if vocals_pcm16.ndim == 1:
		vocals_pcm16 = np.expand_dims(vocals_pcm16, axis=0)

	# Save vocals as a PCM 16-bit WAV file
	logging.info("Saving vocals as a PCM 16-bit WAV file")
	output_path = 'vocals_stem_librosa_highpass.wav'  # Replace with desired output path
	write(output_path, model.samplerate, vocals_pcm16.T)  # Transpose to (samples, channels) format

if __name__ == "__main__":
	main()