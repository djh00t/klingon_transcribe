def generate(transcription, diarization_results, output_path):
    """Generate timecoded text output from transcription and diarization results."""
    with open(output_path, 'w') as f:
        for i, segment in enumerate(diarization_results):
            start_time = segment['start']
            end_time = segment['end']
            text = transcription[i]
            f.write(f"[{start_time}-{end_time}] {text}\n")

def generate_with_speaker(transcription, diarization_results, output_path):
    """Generate timecoded text output with speaker attribution."""
    with open(output_path, 'w') as f:
        for i, segment in enumerate(diarization_results):
            start_time = segment['start']
            end_time = segment['end']
            speaker = segment['label']
            text = transcription[i]
            f.write(f"[{start_time}-{end_time}] Speaker {speaker}: {text}\n")
