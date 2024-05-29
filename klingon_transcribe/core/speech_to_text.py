from nemo.collections.asr.models import ASRModel

def transcribe(audio_path, model_name="Citrinet-1024"):
    """Transcribe audio using the specified ASR model."""
    asr_model = ASRModel.from_pretrained(model_name=model_name)
    transcription = asr_model.transcribe(paths2audio_files=[audio_path])[0]
    return transcription
