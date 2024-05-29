# Klingon Transcribe

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
