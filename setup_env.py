import os

project_structure = {
    "klingon_transcribe/": [
        "__init__.py",
        "cli.py",
        "config.py",
        "core/__init__.py",
        "core/speech_to_text.py",
        "core/diarization.py",
        "preprocessing/__init__.py",
        "preprocessing/audio_enhancement.py",
        "preprocessing/noise_removal.py",
        "storage/__init__.py",
        "storage/local.py",
        "storage/http.py",
        "storage/s3.py",
        "output/__init__.py",
        "output/plain_text.py",
        "output/timecoded_text.py",
        "output/srt.py",
        "api.py",
        "server.py"
    ],
    "tests/": [
        "__init__.py",
        "test_core.py",
        "test_preprocessing.py",
        "test_storage.py",
        "test_output.py"
    ],
    "": [
        ".env.example",
        ".gitignore",
        "Dockerfile",
        "docker-compose.yaml",
        "Makefile",
        "README.md",
        "setup.py",
        "requirements.txt"
    ]
}

# Content for top-level files and __init__.py files
top_level_files_content = {
    ".env.example": """AWS_ACCESS_KEY_ID=<your_aws_access_key>
AWS_SECRET_ACCESS_KEY=<your_aws_secret_key>
HTTP_ACCESS_KEY_ID=<your_http_access_key>
HTTP_SECRET_ACCESS_KEY=<your_http_secret_key>

PREPROCESSING_AUDIO_ENHANCEMENT=true
PREPROCESSING_NOISE_REMOVAL=true
PREPROCESSING_MODEL=denoiser_hifi

CORE_ASR_MODEL=Citrinet-1024
CORE_DIARIZATION_MODEL=speakerdiar_telephony

OUTPUT_FORMATS=plain_text,timecoded_text,timecoded_speaker_text,srt,srt_speaker
""",
    ".gitignore": """__pycache__/
*.pyc
.env
""",
    "Dockerfile": """FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "klingon_transcribe.server:app", "--host", "0.0.0.0", "--port", "8000"]
""",
    "docker-compose.yaml": """version: '3.8'

services:
  klingon_transcribe:
    build: .
    ports:
      - "8000:8000"
    environment:
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - HTTP_ACCESS_KEY_ID=${HTTP_ACCESS_KEY_ID}
      - HTTP_SECRET_ACCESS_KEY=${HTTP_SECRET_ACCESS_KEY}
      - PREPROCESSING_AUDIO_ENHANCEMENT=${PREPROCESSING_AUDIO_ENHANCEMENT}
      - PREPROCESSING_NOISE_REMOVAL=${PREPROCESSING_NOISE_REMOVAL}
      - PREPROCESSING_MODEL=${PREPROCESSING_MODEL}
      - CORE_ASR_MODEL=${CORE_ASR_MODEL}
      - CORE_DIARIZATION_MODEL=${CORE_DIARIZATION_MODEL}
      - OUTPUT_FORMATS=${OUTPUT_FORMATS}
""",
    "Makefile": """install:
\tpip install -r requirements.txt

test:
\tpytest

lint:
\tflake8 klingon_transcribe

clean:
\trm -rf __pycache__
\trm -rf .pytest_cache
\trm -rf .mypy_cache
\trm -rf dist

build:
\tpython setup.py sdist bdist_wheel

docs:
\tpdoc --html --output-dir docs klingon_transcribe
""",
    "README.md": """# Klingon Transcribe

Klingon Transcribe is a Python library for transcribing, diarizing, and enhancing audio files. It provides a CLI, Python API, and FastAPI server interface.

## Features

- **Storage Read Modules**: Local File, HTTP URL, S3 URL
- **Storage Write Modules**: Local File, HTTP URL, S3 URL
- **Output Formats**: Plain Text, Plain Text (Timecoded), Plain Text (Timecoded + Speaker Attributed), SRT, SRT (Speaker Attributed)
- **Preprocessing**: Audio Enhancement, Audio Super Enhancement, Noise Removal, Noise Removal (HiFi)
- **Core**: Speech to Text, Diarization, Diarization (Telephony)

## Installation

pip install -r requirements.txt

## Usage

### CLI

# Run the full pipeline with default configuration
klingon_transcribe run --input s3://bucket/input.wav --output local://output/

# Specify models and steps
klingon_transcribe run --input http://example.com/input.wav --output s3://bucket/output/ --asr-model Citrinet-1024 --diarization-model speakerdiar_telephony --preprocess audio_enhancement noise_removal

# Start the FastAPI server
klingon_transcribe server

### FastAPI

Start the server:

klingon_transcribe server

Send a POST request to \`http://localhost:8000/transcribe/\` with the audio file.

## Development

### Run Tests

make test

### Lint Code

make lint

### Clean Project

make clean

### Build Package

make build

### Generate Documentation

make docs
""",
    "setup.py": """from setuptools import setup, find_packages

setup(
    name='klingon_transcribe',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click',
        'fastapi',
        'uvicorn',
        'boto3',
        'requests',
        'nemo_toolkit',
        'pdoc',
        'pytest',
        'flake8',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'klingon_transcribe=klingon_transcribe.cli:cli',
        ],
    },
)
""",
    "requirements.txt": """click
fastapi
uvicorn
boto3
requests
nemo_toolkit
pdoc
pytest
flake8
python-dotenv
""",
    "klingon_transcribe/__init__.py": '''"""
Klingon Transcribe: A library for transcribing, diarizing, and enhancing audio files.
"""

__version__ = "0.1.0"
''',
    "klingon_transcribe/core/__init__.py": "",
    "klingon_transcribe/preprocessing/__init__.py": "",
    "klingon_transcribe/storage/__init__.py": "",
    "klingon_transcribe/output/__init__.py": "",
    "tests/__init__.py": "",
}

# Function to create directories and files
def create_project_structure(structure, base_path=""):
    for directory, files in structure.items():
        dir_path = os.path.join(base_path, directory) if directory else base_path
        if not dir_path:
            dir_path = '.'
        os.makedirs(dir_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(dir_path, file)
            if not os.path.exists(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                file_content = top_level_files_content.get(file, '')
                f.write(file_content)

create_project_structure(project_structure)

# Define the directory and files for the tests folder
tests_structure = {
    "tests/": [
        "__init__.py",
        "test_core.py",
        "test_preprocessing.py",
        "test_storage.py",
        "test_output.py"
    ]
}

# Content for the test files
test_files_content = {
    "tests/__init__.py": """# This file can be empty
""",
    "tests/test_core.py": """import pytest

def test_transcription():
    assert True  # Replace with actual tests

def test_diarization():
    assert True  # Replace with actual tests
""",
    "tests/test_preprocessing.py": """import pytest

def test_audio_enhancement():
    assert True  # Replace with actual tests

def test_noise_removal():
    assert True  # Replace with actual tests
""",
    "tests/test_storage.py": """import pytest

def test_local_read():
    assert True  # Replace with actual tests

def test_local_write():
    assert True  # Replace with actual tests
""",
    "tests/test_output.py": """import pytest

def test_generate_plain_text():
    assert True  # Replace with actual tests

def test_generate_timecoded_text():
    assert True  # Replace with actual tests
"""
}

# Function to create the tests directory and files
def create_tests_structure(structure, base_path="", content=None):
    for directory, files in structure.items():
        dir_path = os.path.join(base_path, directory)
        os.makedirs(dir_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(dir_path, file)
            with open(file_path, "w") as f:
                if content and file_path in content:
                    f.write(content[file_path])

create_tests_structure(tests_structure, content=test_files_content)

import os

# Define the directory and files for the core folder
core_structure = {
    "klingon_transcribe/core/": [
        "__init__.py",
        "speech_to_text.py",
        "diarization.py"
    ]
}

# Content for the core files
core_files_content = {
    "klingon_transcribe/core/__init__.py": """
# This file can be empty
""",
    "klingon_transcribe/core/speech_to_text.py": """
from nemo.collections.asr.models import ASRModel

def transcribe(audio_path, model_name="Citrinet-1024"):
    \"\"\"Transcribe audio using the specified ASR model.\"\"\"
    asr_model = ASRModel.from_pretrained(model_name=model_name)
    transcription = asr_model.transcribe(paths2audio_files=[audio_path])[0]
    return transcription
""",
    "klingon_transcribe/core/diarization.py": """
from nemo.collections.asr.models import EncDecSpeakerDiarizationModel

def diarize(audio_path, model_name="speakerdiar_telephony"):
    \"\"\"Perform speaker diarization on the audio.\"\"\"
    diarization_model = EncDecSpeakerDiarizationModel.from_pretrained(model_name=model_name)
    diarization_results = diarization_model.diarize(input_file=audio_path)
    return diarization_results
"""
}

# Function to create the core directory and files
def create_core_structure(structure, base_path="", content=None):
    for directory, files in structure.items():
        dir_path = os.path.join(base_path, directory)
        os.makedirs(dir_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(dir_path, file)
            if os.path.exists(file_path):
                with open(file_path, "a") as f:
                    f.write(content[file_path].lstrip('\n'))
            else:
                with open(file_path, "w") as f:
                    f.write(content[file_path].lstrip('\n'))

create_core_structure(core_structure, content=core_files_content)

import os

# Define the directory and files for the output folder
output_structure = {
    "klingon_transcribe/output/": [
        "__init__.py",
        "plain_text.py",
        "timecoded_text.py",
        "srt.py"
    ]
}

# Content for the output files
output_files_content = {
    "klingon_transcribe/output/__init__.py": """# This file can be empty
""",
    "klingon_transcribe/output/plain_text.py": """def generate(transcription, diarization_results, output_path):
    \"\"\"Generate plain text output from transcription and diarization results.\"\"\"
    with open(output_path, 'w') as f:
        f.write(transcription)
""",
    "klingon_transcribe/output/timecoded_text.py": """def generate(transcription, diarization_results, output_path):
    \"\"\"Generate timecoded text output from transcription and diarization results.\"\"\"
    with open(output_path, 'w') as f:
        for i, segment in enumerate(diarization_results):
            start_time = segment['start']
            end_time = segment['end']
            text = transcription[i]
            f.write(f"[{start_time}-{end_time}] {text}\\n")

def generate_with_speaker(transcription, diarization_results, output_path):
    \"\"\"Generate timecoded text output with speaker attribution.\"\"\"
    with open(output_path, 'w') as f:
        for i, segment in enumerate(diarization_results):
            start_time = segment['start']
            end_time = segment['end']
            speaker = segment['label']
            text = transcription[i]
            f.write(f"[{start_time}-{end_time}] Speaker {speaker}: {text}\\n")
""",
    "klingon_transcribe/output/srt.py": """def generate(transcription, diarization_results, output_path):
    \"\"\"Generate SRT output from transcription and diarization results.\"\"\"
    with open(output_path, 'w') as f:
        for i, segment in enumerate(diarization_results):
            start_time = segment['start']
            end_time = segment['end']
            text = transcription[i]
            f.write(f"{i+1}\\n")
            f.write(f"{start_time} --> {end_time}\\n")
            f.write(f"{text}\\n\\n")

def generate_with_speaker(transcription, diarization_results, output_path):
    \"\"\"Generate SRT output with speaker attribution.\"\"\"
    with open(output_path, 'w') as f:
        for i, segment in enumerate(diarization_results):
            start_time = segment['start']
            end_time = segment['end']
            speaker = segment['label']
            text = transcription[i]
            f.write(f"{i+1}\\n")
            f.write(f"{start_time} --> {end_time}\\n")
            f.write(f"Speaker {speaker}: {text}\\n\\n")
"""
}

# Function to create the output directory and files
def create_output_structure(structure, base_path="", content=None):
    for directory, files in structure.items():
        dir_path = os.path.join(base_path, directory)
        os.makedirs(dir_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(dir_path, file)
            if os.path.exists(file_path):
                with open(file_path, "a") as f:
                    f.write(content[file_path].lstrip('\n'))
            else:
                with open(file_path, "w") as f:
                    f.write(content[file_path].lstrip('\n'))

create_output_structure(output_structure, content=output_files_content)

# Define the directory and files for the preprocessing folder
preprocessing_structure = {
    "klingon_transcribe/preprocessing/": [
        "__init__.py",
        "audio_enhancement.py",
        "noise_removal.py"
    ]
}

# Content for the preprocessing files
preprocessing_files_content = {
    "klingon_transcribe/preprocessing/__init__.py": """# This file can be empty""",
    "klingon_transcribe/preprocessing/audio_enhancement.py": """from nemo.collections.tts.models import AudioEnhancerModel

def enhance_audio(audio_path, model_name="AudioSuperRes"):
    \"\"\"Enhance audio using the specified model.\"\"\"
    enhancer_model = AudioEnhancerModel.from_pretrained(model_name=model_name)
    enhanced_audio = enhancer_model.enhance_audio(input_audio_path=audio_path, output_audio_path="enhanced_" + audio_path)
    return enhanced_audio
""",
    "klingon_transcribe/preprocessing/noise_removal.py": """from nemo.collections.asr.models import EncDecSpeakerLabelModel

def remove_noise(audio_path, model_name="denoiser_hifi"):
    \"\"\"Remove noise from audio using the specified model.\"\"\"
    denoiser_model = EncDecSpeakerLabelModel.from_pretrained(model_name=model_name)
    cleaned_audio = denoiser_model.clean_audio(input_audio_path=audio_path, output_audio_path="cleaned_" + audio_path)
    return cleaned_audio
"""
}

# Function to create the preprocessing directory and files
def create_preprocessing_structure(structure, base_path="", content=None):
    for directory, files in structure.items():
        dir_path = os.path.join(base_path, directory)
        os.makedirs(dir_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(dir_path, file)
            if os.path.exists(file_path):
                with open(file_path, "a") as f:
                    f.write(content[file_path].lstrip('\n'))
            else:
                with open(file_path, "w") as f:
                    f.write(content[file_path].lstrip('\n'))

create_preprocessing_structure(preprocessing_structure, content=preprocessing_files_content)


# Define the directory and files for the storage folder
storage_structure = {
    "klingon_transcribe/storage/": [
        "__init__.py",
        "local.py",
        "http.py",
        "s3.py"
    ]
}

# Content for the storage files
storage_files_content = {
    "klingon_transcribe/storage/__init__.py": """# This file can be empty""",
    "klingon_transcribe/storage/local.py": """def read(file_path):
    \"\"\"Read audio file from local storage.\"\"\"
    with open(file_path, 'rb') as f:
        audio_data = f.read()
    return audio_data

def write(file_path, data):
    \"\"\"Write data to local storage.\"\"\"
    with open(file_path, 'wb') as f:
        f.write(data)
""",
    "klingon_transcribe/storage/http.py": """import requests

def read(url):
    \"\"\"Read audio file from HTTP URL.\"\"\"
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def write(url, data):
    \"\"\"Write data to HTTP URL.\"\"\"
    response = requests.put(url, data=data)
    response.raise_for_status()
""",
    "klingon_transcribe/storage/s3.py": """import boto3

s3_client = boto3.client('s3')

def parse_s3_url(s3_url):
    \"\"\"Parse S3 URL to bucket and key.\"\"\"
    assert s3_url.startswith("s3://")
    bucket, key = s3_url[5:].split("/", 1)
    return bucket, key

def read(s3_url):
    \"\"\"Read audio file from S3 URL.\"\"\"
    bucket, key = parse_s3_url(s3_url)
    response = s3_client.get_object(Bucket=bucket, Key=key)
    return response['Body'].read()

def write(s3_url, data):
    \"\"\"Write data to S3 URL.\"\"\"
    bucket, key = parse_s3_url(s3_url)
    s3_client.put_object(Bucket=bucket, Key=key, Body=data)
"""
}

# Function to create the storage directory and files
def create_storage_structure(structure, base_path="", content=None):
    for directory, files in structure.items():
        dir_path = os.path.join(base_path, directory)
        os.makedirs(dir_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(dir_path, file)
            if os.path.exists(file_path):
                with open(file_path, "a") as f:
                    f.write(content[file_path].lstrip('\n'))
            else:
                with open(file_path, "w") as f:
                    f.write(content[file_path].lstrip('\n'))

create_storage_structure(storage_structure, content=storage_files_content)

# Define the directory and files for the klingon_transcribe folder
klingon_transcribe_structure = {
    "klingon_transcribe/": [
        "__init__.py",
        "cli.py",
        "config.py",
        "api.py",
        "server.py"
    ]
}

# Content for the klingon_transcribe files
klingon_transcribe_files_content = {
    "klingon_transcribe/__init__.py": """\"\"\"
Klingon Transcribe: A library for transcribing, diarizing, and enhancing audio files.
\"\"\"

__version__ = "0.1.0"
""",
    "klingon_transcribe/cli.py": """import click
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
    \"\"\"Run the full transcription and diarization pipeline.\"\"\"
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
    \"\"\"Run the FastAPI server.\"\"\"
    import subprocess
    subprocess.run(["uvicorn", "klingon_transcribe.server:app", "--reload"])

if __name__ == '__main__':
    cli()
""",
    "klingon_transcribe/config.py": """import os
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
""",
    "klingon_transcribe/api.py": """from fastapi import FastAPI, UploadFile, Form
from klingon_transcribe.core.speech_to_text import transcribe
from klingon_transcribe.core.diarization import diarize
from klingon_transcribe.preprocessing.audio_enhancement import enhance_audio
from klingon_transcribe.preprocessing.noise_removal import remove_noise
from klingon_transcribe.storage import local, http, s3
from klingon_transcribe.output import plain_text, timecoded_text, srt
import shutil

app = FastAPI()

@app.post("/transcribe/")
async def transcribe_file(file: UploadFile, preprocess: str = Form(None)):
    temp_file = f"temp_{file.filename}"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    audio_data = local.read(temp_file)
    
    # Preprocessing
    if preprocess == 'audio_enhancement':
        audio_data = enhance_audio(audio_data)
    elif preprocess == 'noise_removal':
        audio_data = remove_noise(audio_data)
    
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
""",
    "klingon_transcribe/server.py": """from fastapi import FastAPI, UploadFile, Form
from klingon_transcribe.core.speech_to_text import transcribe
from klingon_transcribe.core.diarization import diarize
from klingon_transcribe.preprocessing.audio_enhancement import enhance_audio
from klingon_transcribe.preprocessing.noise_removal import remove_noise
from klingon_transcribe.storage import local, http, s3
from klingon_transcribe.output import plain_text, timecoded_text, srt
import shutil

app = FastAPI()

@app.post("/transcribe/")
async def transcribe_file(file: UploadFile, preprocess: str = Form(None)):
    temp_file = f"temp_{file.filename}"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    audio_data = local.read(temp_file)
    
    # Preprocessing
    if preprocess == 'audio_enhancement':
        audio_data = enhance_audio(audio_data)
    elif preprocess == 'noise_removal':
        audio_data = remove_noise(audio_data)
    
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
"""
}

# Function to create the klingon_transcribe directory and files
def create_klingon_transcribe_structure(structure, base_path="", content=None):
    for directory, files in structure.items():
        dir_path = os.path.join(base_path, directory)
        os.makedirs(dir_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(dir_path, file)
            if os.path.exists(file_path):
                with open(file_path, "a") as f:
                    f.write(content[file_path].lstrip('\n'))
            else:
                with open(file_path, "w") as f:
                    f.write(content[file_path].lstrip('\n'))

create_klingon_transcribe_structure(klingon_transcribe_structure, content=klingon_transcribe_files_content)