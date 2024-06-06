import numpy as np
from klingon_transcribe.audio_processor import AudioProcessor

def test_only_normalize():
	audio_processor = AudioProcessor()
	audio, sample_rate = audio_processor.load_audio("test_pcm.wav")
	normalized_audio = audio_processor.normalize_audio(audio)
	audio_processor.save_normalized_audio(normalized_audio, "test_only_normalized.wav", sample_rate)

def test_highpass_and_normalize():
	audio_processor = AudioProcessor()
	audio, sample_rate = audio_processor.load_audio("test_pcm.wav")
	normalized_audio = audio_processor.normalize_audio(audio)
	enhanced_audio = audio_processor.enhance_audio_highpass(normalized_audio)
	normalized_audio = audio_processor.normalize_audio(enhanced_audio)
	audio_processor.save_normalized_audio(normalized_audio, "test_highpass_normalized.wav", sample_rate)

def test_demucs_and_normalize():
	audio_processor = AudioProcessor()
	audio, sample_rate = audio_processor.load_audio("test_pcm.wav")
	normalized_audio = audio_processor.normalize_audio(audio)
	enhanced_audio = audio_processor.enhance_audio_demucs(normalized_audio)
	normalized_audio = audio_processor.normalize_audio(enhanced_audio)
	audio_processor.save_normalized_audio(normalized_audio, "test_demucs_normalized.wav", sample_rate)

def test_highpass_normalize_demucs_normalize():
	audio_processor = AudioProcessor()
	audio, sample_rate = audio_processor.load_audio("test_pcm.wav")
	normalized_audio = audio_processor.normalize_audio(audio)
	enhanced_audio = audio_processor.enhance_audio_highpass(normalized_audio)
	normalized_audio = audio_processor.normalize_audio(enhanced_audio)
	enhanced_audio = audio_processor.enhance_audio_demucs(normalized_audio)
	final_normalized_audio = audio_processor.normalize_audio(enhanced_audio)
	audio_processor.save_normalized_audio(final_normalized_audio, "test_highpass_demucs_normalized.wav", sample_rate)

def test_demucs_normalize_highpass_normalize():
	audio_processor = AudioProcessor()
	audio, sample_rate = audio_processor.load_audio("test_pcm.wav")
	normalized_audio = audio_processor.normalize_audio(audio)
	enhanced_audio = audio_processor.enhance_audio_demucs(normalized_audio)
	normalized_audio = audio_processor.normalize_audio(enhanced_audio)
	enhanced_audio = audio_processor.enhance_audio_highpass(normalized_audio)
	final_normalized_audio = audio_processor.normalize_audio(enhanced_audio)
	audio_processor.save_normalized_audio(final_normalized_audio, "test_demucs_highpass_normalized.wav", sample_rate)

def test_normalize_enhance_noisereduce_normalize():
	audio_processor = AudioProcessor()
	audio, sample_rate = audio_processor.load_audio("test_pcm.wav")
	normalized_audio = audio_processor.normalize_audio(audio)
	enhanced_audio = audio_processor.enhance_audio_noisereduce(normalized_audio, sample_rate)
	final_normalized_audio = audio_processor.normalize_audio(enhanced_audio)
	audio_processor.save_normalized_audio(final_normalized_audio, "test_normalize_enhance_noisereduce_normalize.wav", sample_rate)

def test_normalize_highpass_normalize_noisereduce_normalize():
	audio_processor = AudioProcessor()
	audio, sample_rate = audio_processor.load_audio("test_pcm.wav")
	normalized_audio = audio_processor.normalize_audio(audio)
	enhanced_audio = audio_processor.enhance_audio_highpass(normalized_audio)
	normalized_audio = audio_processor.normalize_audio(enhanced_audio)
	enhanced_audio = audio_processor.enhance_audio_noisereduce(normalized_audio, sample_rate)
	final_normalized_audio = audio_processor.normalize_audio(enhanced_audio)
	audio_processor.save_normalized_audio(final_normalized_audio, "test_normalize_highpass_normalize_noisereduce_normalize.wav", sample_rate)

if __name__ == "__main__":
	test_normalize_highpass_normalize_noisereduce_normalize()
	test_only_normalize()
	test_highpass_and_normalize()
	test_demucs_and_normalize()
	test_highpass_normalize_demucs_normalize()
	test_demucs_normalize_highpass_normalize()
	test_normalize_enhance_noisereduce_normalize()



