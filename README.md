# Klingon Transcribe Speech-to-Text & Diarization System

This project provides an end-to-end solution for speech-to-text diarization,
outputting timecoded and speaker attributed text, json and srt files as well as
and a bundle of data for model training and fine-tuning purposes. It is
designed as both a Python library and a FastAPI service.

## Features

- Supports multiple audio formats: WAV, MP3, AAC, FLAC, OGG, WMA, ALAC, AIFF, AMR, AC3, M4A, OPUS.
- Audio preprocessing: Loading, enhancing, and normalizing audio files. 
- Voice Activity Detection (VAD): Detecting segments containing speech.
- Speaker Diarization: Assigning each speech segment to a speaker.
- Speech-to-Text Transcription: Transcribing speech segments to text.
- Transcript Alignment and Formatting: Aligning transcriptions with segments and formatting them for SRT output.
- SRT File Generation: Generating SRT files from formatted transcriptions.
- Training Data Bundle: Generating normalized audio, JSON transcript, speaker
  embeddings, and metadata.
- Flexible file and directory path management. Just use the following
  conventions based on where you want to read/write files from/to:
    - `local://` for local filesystem
    - `http(s)://` for HTTP/HTTPS file locations
    - `s3://` for S3 paths
- Authentication details for S3 and HTTP/HTTPS file locations are saved in the
  docker container environment variables.

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/djh00t/klingon_transcribe.git
cd klingon_transcribe
pip install -r requirements.txt
pip install klingon-file-manager
```

## Usage

### Python Library

You can use the provided classes in your own Python scripts:

```python
from klingon_file_manager import FileManager
from audio_processor import AudioProcessor
from vad import VoiceActivityDetector
from diarizer import SpeakerDiarizer
from transcriber import SpeechToTextTranscriber
from aligner import TranscriptAligner
from output_generator import OutputGenerator

def main(audio_file_path: str, output_srt_path: str, output_txt_path: str, output_data_dir: str):
    # Initialize FileManager
    file_manager = FileManager()

    # Step 1: Audio Preprocessing
    audio_processor = AudioProcessor()
    audio_file = file_manager.manage_file(action='get', path=audio_file_path)['content']
    audio = audio_processor.load_audio(audio_file)
    enhanced_audio = audio_processor.enhance_audio(audio)
    normalized_audio = audio_processor.normalize_audio(enhanced_audio)

    # Save the normalized audio for training purposes
    normalized_audio_path = file_manager.manage_file(action='post', path=output_data_dir, content=normalized_audio)['path']
    audio_processor.save_normalized_audio(normalized_audio, normalized_audio_path)

    # Step 2: Voice Activity Detection
    vad = VoiceActivityDetector(model_path="path_to_vad_model")
    speech_segments = vad.detect_speech_segments(normalized_audio)

    # Step 3: Speaker Diarization
    diarizer = SpeakerDiarizer(model_path="path_to_diarization_model")
    diarized_segments = diarizer.diarize_speakers(normalized_audio, speech_segments)

    # Step 4: Speech-to-Text Transcription
    transcriber = SpeechToTextTranscriber(model_path="path_to_transcription_model")
    transcriptions = transcriber.transcribe_audio(normalized_audio, diarized_segments)

    # Step 5: Alignment and Formatting
    aligner = TranscriptAligner()
    aligned_transcripts = aligner.align_transcripts(diarized_segments, transcriptions)
    srt_content = aligner.format_srt(aligned_transcripts)

    # Step 6: SRT File Generation
    output_generator = OutputGenerator()
    srt_path = file_manager.manage_file(action='post', path=output_srt_path, content=srt_content)['path']
    output_generator.generate_srt(srt_content, srt_path)

    # Generate timestamped text output
    timestamped_text = aligner.generate_timestamped_text(aligned_transcripts)
    with open(output_txt_path, 'w') as txt_file:
        txt_file.write(timestamped_text)

    # Step 7: Generate Data Bundle for Training
    data_bundle_path = file_manager.manage_file(action='post', path=output_data_dir, content=aligned_transcripts)['path']
    output_generator.generate_data_bundle(aligned_transcripts, normalized_audio, data_bundle_path)

if __name__ == "__main__":
    main("path_to_audio_file.wav", "output_subtitles.srt", "output_transcript.txt", "output_data_dir")
```

### FastAPI Service

Run the FastAPI service:

```bash
uvicorn main:app --reload
```

Define a workflow:

```bash
curl -X POST "http://localhost:8000/workflow" -H "Content-Type: application/json" -d '{
  "workflow_name": "default_workflow",
  "steps": [
    {
      "class_name": "AudioProcessor",
      "method_name": "load_audio",
      "params": {"file_path": "/path/to/audio.wav"}
    },
    {
      "class_name": "AudioProcessor",
      "method_name": "enhance_audio",
      "params": {}
    },
    {
      "class_name": "AudioProcessor",
      "method_name": "normalize_audio",
      "params": {}
    },
    {
      "class_name": "VoiceActivityDetector",
      "method_name": "detect_speech_segments",
      "params": {}
    },
    {
      "class_name": "SpeakerDiarizer",
      "method_name": "diarize_speakers",
      "params": {}
    },
    {
      "class_name": "SpeechToTextTranscriber",
      "method_name": "transcribe_audio",
      "params": {}
    },
    {
      "class_name": "TranscriptAligner",
      "method_name": "align_transcripts",
      "params": {}
    },
    {
      "class_name": "TranscriptAligner",
      "method_name": "format_srt",
      "params": {}
    },
    {
      "class_name": "SRTGenerator",
      "method_name": "generate_srt",
      "params": {"output_path": "/path/to/output.srt"}
    },
    {
      "class_name": "DataBundleGenerator",
      "method_name": "generate_data_bundle",
      "params": {"output_data_dir": "/path/to/output_data_dir"}
    }
  ]
}'
```

Process an audio file:

```bash
curl -X POST "http://localhost:8000/process" -H "Content-Type: application/json" -d '{
  "workflow_name": "default_workflow",
  "file_path": "/path/to/audio.wav"
}'
```

List available workflows:

```bash
curl -X GET "http://localhost:8000/workflows"
```

List available workflows:

```bash
curl -X GET "http://localhost:8000/workflows"
```

Get workflow by ID:

```bash
curl -X GET "http://localhost:8000/workflows/{id}"
```

Check the status of a processing job:

```bash
curl -X GET "http://localhost:8000/status"
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
