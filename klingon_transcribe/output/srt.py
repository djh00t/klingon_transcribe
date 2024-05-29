def generate(transcription, diarization_results, output_path):
    """Generate SRT output from transcription and diarization results."""
    with open(output_path, 'w') as f:
        for i, segment in enumerate(diarization_results):
            start_time = segment['start']
            end_time = segment['end']
            text = transcription[i]
            f.write(f"{i+1}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")

def generate_with_speaker(transcription, diarization_results, output_path):
    """Generate SRT output with speaker attribution."""
    with open(output_path, 'w') as f:
        for i, segment in enumerate(diarization_results):
            start_time = segment['start']
            end_time = segment['end']
            speaker = segment['label']
            text = transcription[i]
            f.write(f"{i+1}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"Speaker {speaker}: {text}\n\n")
