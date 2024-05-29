import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    HTTP_ACCESS_KEY_ID = os.getenv('HTTP_ACCESS_KEY_ID')
    HTTP_SECRET_ACCESS_KEY = os.getenv('HTTP_SECRET_ACCESS_KEY')

    PREPROCESSING_AUDIO_ENHANCEMENT = os.getenv('PREPROCESSING_AUDIO_ENHANCEMENT', 'false').lower() == 'true'
    PREPROCESSING_NOISE_REMOVAL = os.getenv('PREPROCESSING_NOISE_REMOVAL', 'false').lower() == 'true'
    PREPROCESSING_MODEL = os.getenv('PREPROCESSING_MODEL', 'denoiser_hifi')

    CORE_ASR_MODEL = os.getenv('CORE_ASR_MODEL', 'Citrinet-1024')
    CORE_DIARIZATION_MODEL = os.getenv('CORE_DIARIZATION_MODEL', 'speakerdiar_telephony')

    OUTPUT_FORMATS = os.getenv('OUTPUT_FORMATS', 'plain_text,timecoded_text,timecoded_speaker_text,srt,srt_speaker').split(',')
