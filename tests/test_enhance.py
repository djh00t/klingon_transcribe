import numpy as np
import soundfile as sf
from klingon_transcribe.audio_processor import AudioProcessor

def load_audio(file_path: str) -> np.ndarray:
    audio, sample_rate = sf.read(file_path)
    if sample_rate != 16000:
        raise ValueError("Audio sample rate must be 16000 Hz")
    return audio

def save_audio(file_path: str, audio: np.ndarray, sample_rate: int = 16000):
    sf.write(file_path, audio, sample_rate)

def test_enhancement_methods():
    audio_file_path = "test_pcm.wav"
    audio = load_audio(audio_file_path)
    audio_processor = AudioProcessor()

    # Test normalize_audio
    normalized_audio = audio_processor.normalize_audio(audio)
    save_audio("normalized_test_pcm.wav", normalized_audio)
    assert len(normalized_audio) == len(audio), "Normalized audio length mismatch"

    # Test highpass_filter_audio
    highpass_audio = audio_processor.highpass_filter_audio(audio)
    save_audio("highpass_test_pcm.wav", highpass_audio)
    assert len(highpass_audio) == len(audio), "Highpass filtered audio length mismatch"

    # Test demucs_enhance_audio
    demucs_audio = audio_processor.demucs_enhance_audio(audio)
    save_audio("demucs_test_pcm.wav", demucs_audio)
    assert len(demucs_audio) == len(audio), "Demucs enhanced audio length mismatch"

if __name__ == "__main__":
    test_enhancement_methods()
    print("All tests passed.")
