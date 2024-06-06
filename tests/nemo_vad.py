import numpy as np
import torch
import matplotlib.pyplot as plt
from nemo.collections.asr.models import EncDecClassificationModel
import soundfile as sf

def load_audio(file_path):
    signal, sample_rate = sf.read(file_path)
    if len(signal.shape) > 1:  # convert to mono
        signal = np.mean(signal, axis=1)
    return signal, sample_rate

def vad_inference(model, audio_signal, sample_rate, device, threshold=0.5):
    # Prepare the audio signal for model input
    audio_signal = torch.tensor(audio_signal, dtype=torch.float32).unsqueeze(0).to(device)  # add batch dimension and move to device
    audio_signal_len = torch.tensor([audio_signal.shape[1]], dtype=torch.int64).to(device)  # length of the audio signal

    # Run the VAD model
    with torch.no_grad():
        logits = model(input_signal=audio_signal, input_signal_length=audio_signal_len)
        predictions = torch.sigmoid(logits)
        vad_segments = (predictions.squeeze().cpu().numpy() > threshold).astype(int)
    
    return vad_segments

def get_speech_segments(vad_segments, sample_rate, frame_duration=0.02):
    speech_segments = []
    start = None
    for i, segment in enumerate(vad_segments):
        if segment == 1 and start is None:
            start = i
        elif segment == 0 and start is not None:
            end = i
            start_time = int(start * frame_duration * 1000)
            end_time = int(end * frame_duration * 1000)
            speech_segments.append((start_time, end_time))
            start = None
    if start is not None:
        speech_segments.append((int(start * frame_duration * 1000), int(len(vad_segments) * frame_duration * 1000)))
    return speech_segments

def plot_waveform_and_segments(audio_signal, sample_rate, speech_segments):
    times = np.arange(len(audio_signal)) / float(sample_rate)

    plt.figure(figsize=(15, 5))
    plt.plot(times, audio_signal, label='Audio Signal')
    for (start_time, end_time) in speech_segments:
        plt.axvspan(start_time / 1000, end_time / 1000, color='red', alpha=0.5, label='Detected Speech')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Waveform with Detected Speech Segments')
    plt.legend(loc='upper right')
    plt.show()

def main():
    audio_path = 'test.wav'

    # Load the VAD model
    vad_model = EncDecClassificationModel.from_pretrained(model_name="vad_multilingual_marblenet")
    vad_model.eval()

    # Determine the device (CPU or CUDA)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    vad_model = vad_model.to(device)

    # Load the audio file
    audio_signal, sample_rate = load_audio(audio_path)

    # Print audio file length in seconds
    audio_length = len(audio_signal) / sample_rate
    print(f"Audio file length: {audio_length:.2f} seconds")

    # Perform VAD inference
    vad_segments = vad_inference(vad_model, audio_signal, sample_rate, device)

    # Process VAD segments to get speech segments
    speech_segments = get_speech_segments(vad_segments, sample_rate)
    print("VAD Segments (start time, end time in milliseconds):", speech_segments)

    # Plot the waveform and detected speech segments
    plot_waveform_and_segments(audio_signal, sample_rate, speech_segments)

if __name__ == "__main__":
    main()
