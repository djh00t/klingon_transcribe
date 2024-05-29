from nemo.collections.asr.models import ClusteringDiarizer as EncDecSpeakerDiarizationModel

def diarize(audio_path, model_name="speakerdiar_telephony"):
    """Perform speaker diarization on the audio."""
    diarization_model = EncDecSpeakerDiarizationModel.from_pretrained(model_name=model_name)
    diarization_results = diarization_model.diarize(input_file=audio_path)
    return diarization_results
