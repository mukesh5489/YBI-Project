# Advanced Speech to Text

This project provides an advanced speech-to-text data collection and recognition tool, developed for the YBI Foundation. It supports both offline (Vosk) and online (Google Web Speech API) speech recognition, and allows you to collect and save audio samples with their transcriptions for training purposes.

## Features

- **Offline Speech Recognition** using the Vosk model.
- **Online Speech Recognition** using Google Web Speech API.
- **Automatic Data Collection:** Saves recognized audio and text pairs for training.
- **Easy Switching** between Vosk and Google APIs.
- **Exit on Command:** Say "goodbye" or "bye" to stop recording (Vosk mode).

## Requirements

- Python 3.7+
- [Vosk Model](https://alphacephei.com/vosk/models) (download and extract to the specified path)
- Packages: `vosk`, `pyaudio`, `speechrecognition`, `soundfile`

Install dependencies:
```bash
pip install vosk pyaudio SpeechRecognition soundfile
```

## Usage

1. **Download a Vosk model** and extract it to the `vosk-model-small-en-us-0.15` directory (or update the path in the script).
2. **Run the script:**
   ```bash
   python advanced_speech_to_text.py
   ```
3. **Choose recognition mode:** Set `USE_VOSK = True` for offline, `False` for Google API.
4. **Speak into your microphone.** Recognized text and audio will be saved in the `training_data/` folder.

## Data Structure

- `training_data/`
  - `sample_0.wav`, `sample_0.txt`
  - `sample_1.wav`, `sample_1.txt`
  - ...

## Credits

Developed for the YBI Foundation.
