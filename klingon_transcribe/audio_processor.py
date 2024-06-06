import numpy as np
import librosa
import soundfile as sf
import noisereduce as nr
from typing import Union, Tuple
from io import BytesIO
from klingon_file_manager import manage_file
import torch
from demucs import pretrained
from demucs.apply import apply_model
import logging

class AudioProcessor:
	def __init__(self):
		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(logging.INFO)


	def load_audio(self, file_path: str) -> Tuple[np.ndarray, int]:
		self.logger.info(f"Loading audio from {file_path}")
		try:
			result = manage_file(action='get', path=file_path)
			if result['status'] != 200:
				self.logger.error(f"Failed to load audio from {file_path}")
				raise ValueError(f"Failed to load audio from {file_path}")
			audio, sample_rate = sf.read(BytesIO(result['content']))
			self.logger.info(f"Loaded audio from {file_path} with sample rate {sample_rate}")
			return audio, sample_rate
		except Exception as e:
			self.logger.exception(f"Exception occurred while loading audio from {file_path}: {e}")
			raise

	def enhance_audio_highpass(self, audio: np.ndarray) -> np.ndarray:
		self.logger.info("Applying high-pass filter to audio")
		try:
			audio_filtered = librosa.effects.preemphasis(audio)
			self.logger.debug("High-pass filter applied successfully")
			return audio_filtered
		except Exception as e:
			self.logger.exception("Exception occurred while applying high-pass filter")
			raise

	def enhance_audio_demucs(self, audio: np.ndarray) -> np.ndarray:
		"""
		Remove music and other loud background noise from the audio using
		Demucs.
		"""
		self.logger.info("Enhancing audio using Demucs")
		try:
			audio_stereo = np.tile(audio, (2, 1))
			audio_stereo = np.expand_dims(audio_stereo, axis=0)

			# Select the model to use options are:
			# htdemucs:	 first version of Hybrid Transformer Demucs. Trained
			#			   on MusDB + 800 songs. Default model.
			# htdemucs_ft:  fine-tuned version of htdemucs, separation will take
			#			   4 times more time but might be a bit better. Same 
			#			   training set as htdemucs.
			# htdemucs_6s:  6 sources version of htdemucs, with piano and guitar 
			#			   being added as sources. Note that the piano source 
			#			   is not working great at the moment.
			# hdemucs_mmi:  Hybrid Demucs v3, retrained on MusDB + 800 songs.
			# mdx:		  trained only on MusDB HQ, winning model on track A
			#			   at the MDX challenge.
			# mdx_extra:	trained with extra training data (including MusDB 
			#			   test set), ranked 2nd on the track B of the MDX 
			#			   challenge.
			# mdx_q, mdx_extra_q: quantized version of the previous models. 
			#			   Smaller download and storage but quality can be 
			#			   slightly worse.
			# SIG:		  where SIG is a single model from the model zoo.
			model = pretrained.get_model('htdemucs')
			model.to('cuda' if torch.cuda.is_available() else 'cpu')
			model.eval()

			waveform_tensor = torch.tensor(audio_stereo, dtype=torch.float32)

			with torch.no_grad():
				sources = apply_model(model, waveform_tensor, split=True, overlap=0.25)[0]

			vocals = sources[3].cpu().numpy()
			vocals = vocals / np.max(np.abs(vocals))
			vocals_mono = vocals.mean(axis=0)

			self.logger.debug("Audio enhanced using Demucs successfully")
			return vocals_mono
		except Exception as e:
			self.logger.exception("Exception occurred while enhancing audio using Demucs")
			raise

	def normalize_audio(self, audio: np.ndarray) -> np.ndarray:
		self.logger.info("Normalizing audio")
		try:
			normalized_audio = librosa.util.normalize(audio)
			self.logger.debug("Audio normalized successfully")
			return normalized_audio
		except Exception as e:
			self.logger.exception("Exception occurred while normalizing audio")
			raise

	def save_normalized_audio(self, audio: np.ndarray, output_path: str, sample_rate: int) -> None:
		self.logger.info(f"Saving normalized audio to {output_path}")
		try:
			sf.write(output_path, audio, samplerate=sample_rate, subtype='PCM_16')
			self.logger.debug(f"Normalized audio saved to {output_path} successfully")
		except Exception as e:
			self.logger.exception(f"Exception occurred while saving normalized audio to {output_path}")
			raise


	def enhance_audio_noisereduce(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
		self.logger.info("Reducing noise from audio using noisereduce")
		try:
			reduced_noise_audio = nr.reduce_noise(y=audio, sr=sample_rate)
			self.logger.debug("Noise reduced successfully")
			return reduced_noise_audio
		except Exception as e:
			self.logger.exception("Exception occurred while reducing noise")
			raise
