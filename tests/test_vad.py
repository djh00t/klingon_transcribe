import librosa
import numpy as np
import soundfile as sf
from klingon_transcribe.vad import VoiceActivityDetector

def load_audio(file_path: str) -> np.ndarray:
    audio, sample_rate = sf.read(file_path)
    if sample_rate != 16000:
        audio = librosa.resample(audio, orig_sr=sample_rate, target_sr=16000)
        sample_rate = 16000
    return audio, sample_rate

def main():
    audio_file_path = "test_pcm.wav"
    audio, original_sample_rate = load_audio(audio_file_path)

    vad = VoiceActivityDetector()

    # NeMo VAD
    nemo_segments = vad.detect_speech_segments_nemo(audio)
    print("NeMo VAD Segments:", nemo_segments)

    # pyannote VAD
    pyannote_segments = vad.detect_speech_segments_pyannote(audio)
    print("pyannote VAD Segments:", pyannote_segments)

    # WebRTC VAD
    webrtc_segments = [(int(start * original_sample_rate / 16000), int(end * original_sample_rate / 16000)) for start, end in webrtc_segments]
    print("WebRTC VAD Segments:", webrtc_segments)

if __name__ == "__main__":
    main()
