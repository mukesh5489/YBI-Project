import speech_recognition as sr
import os
import soundfile as sf
from vosk import Model, KaldiRecognizer
import queue
import pyaudio
import json
import wave
TRAINING_DATA_DIR = "training_data"
USE_VOSK = True  # Set to False to use Google Web Speech API
VOSK_MODEL_PATH = r"c:\\Users\\mukes\\Documents\\Coding\\MY_WORK\\YBI\\vosk-model-small-en-us-0.15"  

os.makedirs(TRAINING_DATA_DIR, exist_ok=True)

def save_training_sample(audio_data, transcript, sample_id):
    wav_path = os.path.join(TRAINING_DATA_DIR, f"sample_{sample_id}.wav")
    txt_path = os.path.join(TRAINING_DATA_DIR, f"sample_{sample_id}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(transcript)
    audio_data.export(wav_path, format="wav")
    print(f"Saved training sample: {wav_path}, {txt_path}")

def recognize_with_vosk():
    if not os.path.exists(VOSK_MODEL_PATH):
        print(f"Please download the Vosk model and extract it to: {VOSK_MODEL_PATH}")
        return
    model = Model(VOSK_MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()
    print("Listening (Vosk)... Press Ctrl+C to stop.")
    frames = []
    try:
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            frames.append(data)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result)["text"]
                print("Recognized:", text)
                if text.strip():
                    # Save audio and text for training
                    sample_id = len(os.listdir(TRAINING_DATA_DIR)) // 2
                    wav_path = os.path.join(TRAINING_DATA_DIR, f"sample_{sample_id}.wav")
                    with open(wav_path, "wb") as wf:
                        wf.write(b"".join(frames))
                    with open(os.path.join(TRAINING_DATA_DIR, f"sample_{sample_id}.txt"), "w", encoding="utf-8") as f:
                        f.write(text)
                    print(f"Saved training sample: {wav_path}")
                    
                    if any(word in text.lower() for word in ["goodbye", "bye"]):
                        print("Exit phrase detected. Exiting...")
                        break
                frames = []
    except KeyboardInterrupt:
        print("Stopped.")
    stream.stop_stream()
    stream.close()
    p.terminate()

def recognize_with_google():
    r = sr.Recognizer()
    mic = sr.Microphone()
    print("Listening (Google Web Speech API)... Press Ctrl+C to stop.")
    sample_id = len(os.listdir(TRAINING_DATA_DIR)) // 2
    try:
        while True:
            with mic as source:
                r.adjust_for_ambient_noise(source)
                print("Say something...")
                audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                print("Recognized:", text)
                # Save audio and text for training
                wav_path = os.path.join(TRAINING_DATA_DIR, f"sample_{sample_id}.wav")
                with open(wav_path, "wb") as f:
                    f.write(audio.get_wav_data())
                with open(os.path.join(TRAINING_DATA_DIR, f"sample_{sample_id}.txt"), "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"Saved training sample: {wav_path}")
                sample_id += 1
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"API error: {e}")
    except KeyboardInterrupt:
        print("Stopped.")

def main():
    if USE_VOSK:
        recognize_with_vosk()
    else:
        recognize_with_google()

if __name__ == "__main__":
    main()
