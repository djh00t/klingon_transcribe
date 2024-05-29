def generate(transcription, diarization_results, output_path):
    """Generate plain text output from transcription and diarization results."""
    with open(output_path, 'w') as f:
        f.write(transcription)
