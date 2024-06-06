# Architecture

## Overview

The Speech-to-Text Diarization System is designed as a modular and extensible architecture that can be used as both a Python library and a FastAPI service. The system supports configurable workflows defined via JSON and includes logging for traceability.

## Components

### AudioProcessor
- **Methods**:
  - `load_audio(file_path: str) -> np.ndarray` (supports the following prefixes: `local://` for local filesystem, `http(s)://` for HTTP/HTTPS file locations, `s3://` for S3 paths)
  - `enhance_audio(audio: np.ndarray) -> np.ndarray`
  - `normalize_audio(audio: np.ndarray) -> np.ndarray`
  - `save_normalized_audio(audio: np.ndarray, output_dir: str) -> None`
- **Logging**:
  - Logs audio loading, enhancement, and normalization steps.
- **Inputs/Outputs**:
  - Input: `file_path` (str)
  - Output: `normalized_audio` (np.ndarray)

### VoiceActivityDetector
- **Methods**:
  - `detect_speech_segments(audio: np.ndarray) -> List[Tuple[int, int]]`
- **Logging**:
  - Logs detection of speech segments.
- **Inputs/Outputs**:
  - Input: `audio` (np.ndarray)
  - Output: `segments` (List[Tuple[int, int]])

### SpeakerDiarizer
- **Methods**:
  - `diarize_speakers(audio: np.ndarray, segments: List[Tuple[int, int]]) -> List[Tuple[int, int, int]]`
- **Logging**:
  - Logs diarization of speech segments.
- **Inputs/Outputs**:
  - Input: `audio` (np.ndarray), `segments` (List[Tuple[int, int]])
  - Output: `diarized_segments` (List[Tuple[int, int, int]])

### SpeechToTextTranscriber
- **Methods**:
  - `transcribe_audio(audio: np.ndarray, segments: List[Tuple[int, int]]) -> List[str]`
- **Logging**:
  - Logs transcription of audio segments.
- **Inputs/Outputs**:
  - Input: `audio` (np.ndarray), `segments` (List[Tuple[int, int]])
  - Output: `transcriptions` (List[str])

### TranscriptAligner
- **Methods**:
  - `align_transcripts(segments: List[Tuple[int, int, int]], transcriptions: List[str]) -> List[Tuple[int, int, int, str]]`
  - `format_srt(aligned_transcripts: List[Tuple[int, int, int, str]]) -> str`
  - `generate_timestamped_text(aligned_transcripts: List[Tuple[int, int, int, str]]) -> str`
- **Logging**:
  - Logs alignment and formatting steps.
- **Inputs/Outputs**:
  - Input: `segments` (List[Tuple[int, int, int]]), `transcriptions` (List[str])
  - Output: `aligned_transcripts` (List[Tuple[int, int, int, str]]), `srt_content` (str), `timestamped_text` (str)

### SRTGenerator
- **Methods**:
  - `generate_srt(srt_content: str, output_path: str) -> None`
- **Logging**:
  - Logs SRT generation.
- **Inputs/Outputs**:
  - Input: `srt_content` (str), `output_path` (str)
  - Output: None

### OutputGenerator
- **Methods**:
  - `generate_data_bundle(aligned_transcripts: List[Tuple[int, int, int, str]], audio: np.ndarray, output_dir: str) -> None`
  - `generate_srt(aligned_transcripts: List[Tuple[int, int, int, str]], output_path: str) -> None`
- **Logging**:
  - Logs output generation steps.
- **Inputs/Outputs**:
  - Input: `aligned_transcripts` (List[Tuple[int, int, int, str]]), `audio` (np.ndarray), `output_dir` (str)
  - Output: 
    - Normalized audio file
    - JSON transcript
    - Speaker embeddings
    - Metadata
    - SRT file (if `generate_srt` is called)

## Data Flow

1. **Audio Input**: The input audio file is loaded and processed by the `AudioProcessor`.
2. **Speech Segments**: `VoiceActivityDetector` identifies segments containing speech.
3. **Diarization**: `SpeakerDiarizer` assigns each segment to a speaker.
4. **Transcription**: `SpeechToTextTranscriber` converts the audio segments to text.
5. **Alignment**: `TranscriptAligner` aligns the transcriptions with the segments and formats them for SRT.
6. **SRT Output**: `SRTGenerator` writes the formatted transcriptions to an SRT file.
7. **Data Bundle**: `DataBundleGenerator` saves normalized audio, JSON transcript, speaker embeddings, and metadata for training purposes.

## JSON API

### Define a Workflow

```json
{
  "workflow_name": "default_workflow",
  "steps": [
    {
      "class_name": "AudioProcessor",
      "method_name": "load_audio",
      "params": {"file_path": "local:///path/to/audio.wav"}
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
      "params": {"output_path": "local:///path/to/output.srt"}
    },
    {
      "class_name": "DataBundleGenerator",
      "method_name": "generate_data_bundle",
      "params": {"output_data_dir": "local:///path/to/output_data_dir"}
    }
  ]
}
```

### Process an Audio File

```json
{
  "workflow_name": "default_workflow",
  "file_path": "/path/to/audio.wav"
}
```

### List Available Workflows

```json
{
  "workflows": ["default_workflow", "custom_workflow"]
}
```

### Get Workflow by ID

```json
{
  "workflow_name": "default_workflow",
  "steps": [
    {"class_name": "AudioProcessor", "method_name": "load_audio", "params": {"file_path": "/path/to/audio.wav"}},
    {"class_name": "AudioProcessor", "method_name": "enhance_audio", "params": {}},
    {"class_name": "AudioProcessor", "method_name": "normalize_audio", "params": {}},
    {"class_name": "VoiceActivityDetector", "method_name": "detect_speech_segments", "params": {}},
    {"class_name": "SpeakerDiarizer", "method_name": "diarize_speakers", "params": {}},
    {"class_name": "SpeechToTextTranscriber", "method_name": "transcribe_audio", "params": {}},
    {"class_name": "TranscriptAligner", "method_name": "align_transcripts", "params": {}},
    {"class_name": "TranscriptAligner", "method_name": "format_srt", "params": {}},
    {"class_name": "OutputGenerator", "method_name": "generate_srt", "params": {"output_path": "/path/to/output.srt"}},
    {"class_name": "OutputGenerator", "method_name": "generate_data_bundle", "params": {"output_data_dir": "/path/to/output_data_dir"}}
  ]
}
```

### Check Job Status

```json
{
  "job_id": "unique_job_id"
}
```

## Conclusion

This architecture document outlines the design of a modular and extensible speech-to-text diarization system, supporting configurable workflows and providing both a Python library and a FastAPI service for various use cases. It includes support for generating a data bundle for training purposes, consisting of normalized audio, JSON transcript, speaker embeddings, and metadata.
