from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Tuple, Dict, Any
import uvicorn

from audio_processor import AudioProcessor
from vad import VoiceActivityDetector
from diarizer import SpeakerDiarizer
from transcriber import SpeechToTextTranscriber
from aligner import TranscriptAligner
from output_generator import OutputGenerator
from data_bundle_generator import DataBundleGenerator

app = FastAPI(
    title="Speech-to-Text Diarization API",
    description="This API provides endpoints for speech-to-text diarization, including audio processing, voice activity detection, speaker diarization, transcription, alignment, and SRT generation.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "workflows",
            "description": "Operations with workflows."
        },
        {
            "name": "process",
            "description": "Operations for processing audio files."
        },
        {
            "name": "status",
            "description": "Operations for checking job status."
        }
    ]
)

class WorkflowStep(BaseModel):
    class_name: str
    method_name: str
    params: Dict[str, Any]

class Workflow(BaseModel):
    workflow_name: str
    steps: List[WorkflowStep]

class ProcessRequest(BaseModel):
    workflow_name: str
    file_path: str

class StatusRequest(BaseModel):
    job_id: str

workflows = {}

@app.post("/workflow", tags=["workflows"])
def define_workflow(workflow: Workflow):
    workflows[workflow.workflow_name] = workflow.steps
    return {"workflow_id": workflow.workflow_name}

@app.get("/workflows", tags=["workflows"])
def list_workflows():
    return {"workflows": list(workflows.keys())}

@app.get("/workflows/{id}", tags=["workflows"])
def get_workflow(id: str):
    if id not in workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {"workflow_name": id, "steps": workflows[id]}

@app.post("/process", tags=["process"])
def process_audio(request: ProcessRequest):
    if request.workflow_name not in workflows:
        raise HTTPException(status_code=400, detail="Workflow not found")

    # Simulate job processing
    job_id = "unique_job_id"
    return {"job_id": job_id}

@app.get("/status", tags=["status"])
def check_status(request: StatusRequest):
    # Simulate job status check
    return {"status": "completed", "progress": 100}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
