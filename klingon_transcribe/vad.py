import numpy as np
from typing import List, Tuple
import webrtcvad
import torch
from pyannote.audio.pipelines import VoiceActivityDetection
from nemo.collections.asr.models import EncDecClassificationModel
import logging
import os
from klingon_transcribe.utils import GPUTools

class VoiceActivityDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def detect_speech_segments_nemo(self, audio: np.ndarray, model_name: str = "vad_multilingual_marblenet") -> List[Tuple[int, int]]:
        self.logger.info("Loading NeMo model from %s", model_name)
        # Load the NeMo model
        nemo_vad = EncDecClassificationModel.from_pretrained(model_name)
        nemo_vad.eval()
        nemo_vad = nemo_vad.to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

        # Convert the audio to a tensor
        audio_tensor = torch.from_numpy(audio).float().unsqueeze(0).to(nemo_vad.device)

        # Run the VAD model
        input_signal_length = torch.tensor([audio_tensor.shape[1]]).to(nemo_vad.device)
        logits = nemo_vad.forward(input_signal=audio_tensor, input_signal_length=input_signal_length)
        self.logger.debug("Logits shape: %s", logits.shape)
        probs = torch.sigmoid(logits).squeeze().cpu().detach().numpy()
        self.logger.debug("Probabilities shape: %s", probs.shape)
        self.logger.debug("Probabilities: %s", probs)

        # Detect speech segments
        self.logger.info("Starting speech segment detection using NeMo model")
        segments = []
        in_segment = False
        start = 0
        for i, prob in enumerate(probs):
            if prob > 0.5 and not in_segment:
                start = i
                in_segment = True
            elif prob <= 0.5 and in_segment:
                segments.append((start, i))
                in_segment = False
        if in_segment:
            segments.append((start, len(probs)))

        self.logger.info("Detected %d speech segments using NeMo model", len(segments))
        return segments
        
    def detect_speech_segments_pyannote(self, audio: np.ndarray, model_name: str = "pyannote/segmentation") -> List[Tuple[int, int]]:
        self.logger.info("Loading pyannote model from %s", model_name)
        device = GPUTools.get_best_device()
        self.logger.info("Using device: %s", device)

        # Set the device for PyTorch
        torch_device = torch.device(device)

        # import the HF_HUB_TOKEN from the environment
        HF_HUB_TOKEN = os.getenv("HF_HUB_TOKEN")

        if HF_HUB_TOKEN is None:
            raise ValueError("HF_HUB_TOKEN is not set. Please set the Hugging Face Hub token.")
        
        # Load the pyannote model with authentication token if provided
        pyannote_vad = VoiceActivityDetection(model_name, use_auth_token=HF_HUB_TOKEN)
        pyannote_vad.to(torch_device)
        
        audio = {"waveform": torch.from_numpy(audio).float().unsqueeze(0), "sample_rate": 16000}
        vad_output = pyannote_vad(audio)
        self.logger.debug("pyannote VAD output obtained")

        self.logger.info("Starting speech segment detection using pyannote model")
        segments = []
        for segment in vad_output.get_timeline().support():
            start, end = segment.start, segment.end
            segments.append((int(start * 16000), int(end * 16000)))

        self.logger.info("Detected %d speech segments using pyannote model", len(segments))
        return segments

    def detect_speech_segments_webrtcvad(self, audio: np.ndarray) -> List[Tuple[int, int]]:
        self.logger.info("Initializing WebRTC VAD")
        device = GPUTools.get_best_device()
        self.logger.info("Using device: %s", device)
        

        webrtc_vad = webrtcvad.Vad()
        webrtc_vad.set_mode(3)

        sample_rate = 16000
        frame_duration = 30  # ms
        frame_length = (int(sample_rate * frame_duration / 1000) // 320) * 320  # Adjust frame length to be a multiple of 320
        audio_bytes = audio.tobytes()

        self.logger.info("Starting speech segment detection using WebRTC VAD")
        segments = []
        in_segment = False
        start = 0
        for i in range(0, len(audio_bytes), frame_length):
            frame = audio_bytes[i:i + frame_length]
            if len(frame) < frame_length:
                break
            is_speech = webrtc_vad.is_speech(frame, sample_rate)
            if is_speech and not in_segment:
                start = i // 2
                in_segment = True
            elif not is_speech and in_segment:
                segments.append((start, i // 2))
                in_segment = False
        if in_segment:
            segments.append((start, len(audio) // 2))

        self.logger.info("Detected %d speech segments using WebRTC VAD", len(segments))
        return segments
