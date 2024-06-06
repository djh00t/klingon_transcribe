## API Schema

This document provides a detailed schema for the Speech-to-Text Diarization System API. The API supports both GET and POST methods for various endpoints, allowing users to define workflows, process audio files, and check job statuses.

### API Information

- **API Name**: Speech-to-Text Diarization API
- **API Version**: 1.0.0
- **API Description**: This API provides endpoints for speech-to-text diarization, including audio processing, voice activity detection, speaker diarization, transcription, alignment, and SRT generation.

### Endpoints

#### List Available Workflows

- **Endpoint**: `/workflows`
- **Methods**: `GET`
- **Request Parameters**:
  - None

- **Response Parameters**:
  - **200**:
    - `description`: Success
    - `schema`:
      - `workflows` (array of strings): List of available workflows.
  - **400**:
    - `description`: Bad Request
    - `schema`:
      - `error_code` (string): Error code
      - `error_message` (string): Error message

- **Error Codes**:
  - `ERR006`: Unable to retrieve workflows

- **Example**:
  ```json
  {
    "workflows": ["default_workflow", "custom_workflow"]
  }
  ```

#### Get Workflow by ID

- **Endpoint**: `/workflows/{id}`
- **Methods**: `GET`
- **Request Parameters**:
  - **GET**:
    - `id` (string, required): The unique ID of the workflow.

- **Response Parameters**:
  - **200**:
    - `description`: Success
    - `schema`:
      - `workflow` (object): The content of the requested workflow.
  - **404**:
    - `description`: Not Found
    - `schema`:
      - `error_code` (string): Error code
      - `error_message` (string): Error message

- **Error Codes**:
  - `ERR007`: Workflow not found

- **Example**:
  ```json
  {
    "workflow_name": "default_workflow",
    "steps": [
      {"class_name": "AudioProcessor", "method_name": "load_audio", "params": {"file_path": "local:///path/to/audio.wav"}},
      {"class_name": "AudioProcessor", "method_name": "enhance_audio", "params": {}},
      {"class_name": "AudioProcessor", "method_name": "normalize_audio", "params": {}},
      {"class_name": "VoiceActivityDetector", "method_name": "detect_speech_segments", "params": {}},
      {"class_name": "SpeakerDiarizer", "method_name": "diarize_speakers", "params": {}},
      {"class_name": "SpeechToTextTranscriber", "method_name": "transcribe_audio", "params": {}},
      {"class_name": "TranscriptAligner", "method_name": "align_transcripts", "params": {}},
      {"class_name": "TranscriptAligner", "method_name": "format_srt", "params": {}},
      {"class_name": "OutputGenerator", "method_name": "generate_srt", "params": {"output_path": "local:///path/to/output.srt"}},
      {"class_name": "OutputGenerator", "method_name": "generate_data_bundle", "params": {"output_data_dir": "local:///path/to/output_data_dir"}}
    ]
  }
  ```

#### Define a Workflow

- **Endpoint**: `/workflow`
- **Methods**: `POST`
- **Request Parameters**:
  - **POST**:
    - `workflow_name` (string, required): The name of the workflow.
    - `steps` (array, required): An array of steps defining the workflow.
      - Each step includes:
        - `class_name` (string, required): The class name of the component.
        - `method_name` (string, required): The method name to be called.
        - `params` (object, optional): Parameters for the method.

- **Response Parameters**:
  - **200**:
    - `description`: Success
    - `schema`:
      - `workflow_id` (string): The unique ID of the defined workflow.
  - **400**:
    - `description`: Bad Request
    - `schema`:
      - `error_code` (string): Error code
      - `error_message` (string): Error message

- **Error Codes**:
  - `ERR001`: Invalid workflow definition
  - `ERR002`: Missing required parameters

- **Example**:
  ```json
  {
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
  }
  ```

#### Process an Audio File

- **Endpoint**: `/process`
- **Methods**: `POST`
- **Request Parameters**:
  - **POST**:
    - `workflow_name` (string, required): The name of the workflow to be executed.
    - `file_path` (string, required): The path to the audio file to be processed. Supports the following prefixes:
      - `local://` for local filesystem
      - `http(s)://` for HTTP/HTTPS file locations
      - `s3://` for S3 paths

- **Response Parameters**:
  - **200**:
    - `description`: Success
    - `schema`:
      - `job_id` (string): The unique ID of the processing job.
  - **400**:
    - `description`: Bad Request
    - `schema`:
      - `error_code` (string): Error code
      - `error_message` (string): Error message

- **Error Codes**:
  - `ERR003`: Workflow not found
  - `ERR004`: Invalid audio file path

- **Example**:
  ```json
  {
    "workflow_name": "default_workflow",
    "file_path": "/path/to/audio.wav"
  }
  ```



#### Check Job Status

- **Endpoint**: `/status`
- **Methods**: `GET`
- **Request Parameters**:
  - **GET**:
    - `job_id` (string, required): The unique ID of the processing job.

- **Response Parameters**:
  - **200**:
    - `description`: Success
    - `schema`:
      - `status` (string): The current status of the job.
      - `progress` (integer): The progress percentage of the job.
  - **400**:
    - `description`: Bad Request
    - `schema`:
      - `error_code` (string): Error code
      - `error_message` (string): Error message

- **Error Codes**:
  - `ERR005`: Job not found

- **Example**:
  ```json
  {
    "job_id": "unique_job_id"
  }
  ```

### API Monitoring

- **Logging**:
  - **Description**: Details on what will be logged.
  - **Fields**: `timestamp`, `request_id`, `endpoint`, `response_time`

### API Testing

- **Description**: Testing strategies and tools.
- **Tools**: `Pytest`, `Postman`

### API Documentation

- **Description**: Documentation details and tools.
- **Tools**: `Swagger`, `pdoc`

### API Usage Examples

#### Example of using the GET method

- **Request**:
  ```json
  {
    "method": "GET",
    "url": "/status",
    "parameters": {
      "job_id": "unique_job_id"
    }
  }
  ```
- **Response**:
  ```json
  {
    "status": 200,
    "body": {
      "status": "completed",
      "progress": 100
    }
  }
  ```

#### Example of using the POST method

- **Request**:
  ```json
  {
    "method": "POST",
    "url": "/process",
    "body": {
      "workflow_name": "default_workflow",
      "file_path": "/path/to/audio.wav"
    }
  }
  ```
- **Response**:
  ```json
  {
    "status": 200,
    "body": {
      "job_id": "unique_job_id"
    }
  }
  ```
