feat: add audio dynamic range compression notebook

This notebook demonstrates how to apply dynamic range compression to audio using the `librosa` library. It includes steps to:
 1. Load and preprocess an audio file.
 2. Apply dynamic range compression to the audio.
 3. Visualize and output the compressed audio.

Dynamic range compression reduces the volume of loud sounds and amplifies quieter sounds, resulting in a more consistent audio level. This can be useful for speech-to-text processing as it ensures that all parts of the speech are audible, even if the speaker's volume varies.


feat: add high-pass filter audio processing notebook
This notebook demonstrates how to apply a high-pass filter to an audio file using the `librosa` library. It includes steps to:

 1. Load and preprocess an audio file.
 2. Apply the high-pass filter.
 3. Visualize and output the filtered audio.
 
A high-pass filter allows frequencies above a certain cutoff frequency to pass through while attenuating frequencies below the cutoff. This can be useful for removing low-frequency noise such as hums or rumbles, which can interfere with speech clarity.

feat: add noise reduction audio processing notebook

This notebook demonstrates how to reduce noise in audio using the `noisereduce` library. It includes steps to:
 1. Load and preprocess an audio file.   
 2. Apply noise reduction to the audio.   
 3. Visualize and output the noise-reduced audio.

Noise reduction is useful for removing background noise from audio recordings, improving the clarity of speech, and making it easier for speech-to-text systems to accurately transcribe the audio.


feat: add audio normalization notebook

This notebook demonstrates how to normalize audio using the `librosa` library. It includes steps to:

 1. Load and preprocess an audio file.   
 2. Apply normalization to the audio.     
 3. Visualize and output the normalized audio.

Normalization adjusts the audio signal to a standard level of loudness, ensuring consistent volume, which is beneficial for speech-to-text processing. 



feat: add VAD (Voice Activity Detection) notebook

This notebook demonstrates how to apply Voice Activity Detection (VAD) using the `nemo` library. It includes steps to:
1. Load and preprocess an audio file.
2. Apply VAD to detect speech segments.
3. Visualize and output the detected speech segments.

VAD is useful for identifying and isolating speech segments in an audio file, which can be beneficial for various speech processing tasks such as transcription and speaker diarization.

feat: add VAD (Voice Activity Detection) notebook using pyannote

This notebook demonstrates how to apply Voice Activity Detection (VAD) using the `pyannote` library. It includes steps to:
1. Load and preprocess an audio file.
2. Apply VAD to detect speech segments.
3. Visualize and output the detected speech segments.

Using `pyannote` for VAD helps in accurately identifying speech segments, which is crucial for tasks like transcription, speaker diarization, and other speech processing applications.

feat: add VAD (Voice Activity Detection) notebook using silero

This notebook demonstrates how to apply Voice Activity Detection (VAD) using the `silero` library. It includes steps to:
1. Load and preprocess an audio file.
2. Apply VAD to detect speech segments.
3. Visualize and output the detected speech segments.

Using `silero` for VAD provides an efficient and accurate method for identifying speech segments, which is essential for tasks such as transcription, speaker diarization, and other speech processing applications.

feat: add VAD (Voice Activity Detection) notebook using webrtcvad

This notebook demonstrates how to apply Voice Activity Detection (VAD) using the `webrtcvad` library. It includes steps to:
1. Load and preprocess an audio file.
2. Apply VAD to detect speech segments.
3. Visualize and output the detected speech segments.

Using `webrtcvad` for VAD offers a lightweight and efficient method for identifying speech segments, which is crucial for tasks such as transcription, speaker diarization, and other speech processing applications.
