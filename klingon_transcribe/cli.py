import click
from klingon_transcribe.core.speech_to_text import transcribe
from klingon_transcribe.core.diarization import diarize
from klingon_transcribe.preprocessing.audio_enhancement import enhance_audio
from klingon_transcribe.preprocessing.noise_removal import remove_noise
from klingon_transcribe.storage import local, http, s3
from klingon_transcribe.output import plain_text, timecoded_text, srt

@click.group()
def cli():
    pass

@cli.command()
@click.option('--input', required=True, help='Input audio file path (local, HTTP, or S3 URL).')
@click.option('--output', required=True, help='Output file path (local, HTTP, or S3 URL).')
@click.option('--asr-model', default='Citrinet-1024', help='ASR model to use.')
@click.option('--diarization-model', default='speakerdiar_telephony', help='Diarization model to use.')
@click.option('--preprocess', multiple=True, type=click.Choice(['audio_enhancement', 'noise_removal']), help='Preprocessing steps to apply.')
@click.option('--output-formats', multiple=True, type=click.Choice(['plain_text', 'timecoded_text', 'timecoded_speaker_text', 'srt', 'srt_speaker']), help='Output formats to generate.')
def run(input, output, asr_model, diarization_model, preprocess, output_formats):
    """Run the full transcription and diarization pipeline."""
    # Determine storage type and read audio
    if input.startswith('s3://'):
        audio_data = s3.read(input)
    elif input.startswith('http://') or input.startswith('https://'):
        audio_data = http.read(input)
    else:
        audio_data = local.read(input)
    
    # Preprocessing
    if 'audio_enhancement' in preprocess:
        audio_data = enhance_audio(audio_data)
    if 'noise_removal' in preprocess:
        audio_data = remove_noise(audio_data)

    # Core processing
    transcription = transcribe(audio_data, model_name=asr_model)
    diarization_results = diarize(audio_data, model_name=diarization_model)
    
    # Output processing
    for fmt in output_formats:
        if fmt == 'plain_text':
            plain_text.generate(transcription, diarization_results, output)
        elif fmt == 'timecoded_text':
            timecoded_text.generate(transcription, diarization_results, output)
        elif fmt == 'timecoded_speaker_text':
            timecoded_text.generate_with_speaker(transcription, diarization_results, output)
        elif fmt == 'srt':
            srt.generate(transcription, diarization_results, output)
        elif fmt == 'srt_speaker':
            srt.generate_with_speaker(transcription, diarization_results, output)

@cli.command()
def server():
    """Run the FastAPI server."""
    import subprocess
    subprocess.run(["uvicorn", "klingon_transcribe.server:app", "--reload"])

if __name__ == '__main__':
    cli()
