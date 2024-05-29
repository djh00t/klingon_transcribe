from nemo.collections.audio.models import AudioEnhancerModel

def enhance_audio(audio_path, model_name="AudioSuperRes"):
    """Enhance audio using the specified model."""
    enhancer_model = AudioEnhancerModel.from_pretrained(model_name=model_name)
    enhanced_audio = enhancer_model.enhance_audio(input_audio_path=audio_path, output_audio_path="enhanced_" + audio_path)
    return enhanced_audio
