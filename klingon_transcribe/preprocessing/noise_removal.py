from nemo.collections.asr.models import EncDecSpeakerLabelModel

def remove_noise(audio_path, model_name="denoiser_hifi"):
    """Remove noise from audio using the specified model."""
    denoiser_model = EncDecSpeakerLabelModel.from_pretrained(model_name=model_name)
    cleaned_audio = denoiser_model.clean_audio(input_audio_path=audio_path, output_audio_path="cleaned_" + audio_path)
    return cleaned_audio
