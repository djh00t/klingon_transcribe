from fastapi import FastAPI, UploadFile, Form
from klingon_transcribe.core.speech_to_text import transcribe
from klingon_transcribe.core.diarization import diarize
from klingon_transcribe.storage import local, http, s3
from klingon_transcribe.output import plain_text, timecoded_text, srt
import shutil

app = FastAPI()

@app.post("/transcribe/")
async def transcribe_file(file: UploadFile):
    temp_file = f"temp_{file.filename}"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    audio_data = local.read(temp_file)
    
    
    transcription = transcribe(audio_data)
    diarization_results = diarize(audio_data)

    plain_text_output = plain_text.generate(transcription, diarization_results, "plain_text.txt")
    timecoded_text_output = timecoded_text.generate(transcription, diarization_results, "timecoded_text.txt")
    srt_output = srt.generate(transcription, diarization_results, "output.srt")
    
    response = {
        "plain_text": plain_text_output,
        "timecoded_text": timecoded_text_output,
        "srt": srt_output
    }

    return response
