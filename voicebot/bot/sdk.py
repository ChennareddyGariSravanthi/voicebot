import requests
import openai
from pydub import AudioSegment
import io
import sounddevice as sd
import numpy as np
import time

def setup(stt_key, tts_key, llm_key):
    global DEEPGRAM_API_KEY, TTS_API_KEY, OPENAI_API_KEY
    DEEPGRAM_API_KEY = stt_key
    TTS_API_KEY = tts_key
    OPENAI_API_KEY = llm_key
    openai.api_key = OPENAI_API_KEY

def audio_to_text(audio_file):
    response = requests.post(
        'https://api.deepgram.com/v1/listen',
        headers={'Authorization': f'Token {DEEPGRAM_API_KEY}'},
        files={'file': audio_file},
    )
    response.raise_for_status()
    return response.json().get('results', [{}])[0].get('alternatives', [{}])[0].get('transcript', '')

def get_openai_response(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def text_to_audio(text):
    tts_url = 'https://api.your-tts-service.com/generate'
    response = requests.post(
        tts_url,
        headers={'Authorization': f'Bearer {TTS_API_KEY}'},
        json={'text': text}
    )
    response.raise_for_status()
    return io.BytesIO(response.content)

def stream_conversation(audio_file):
    text = audio_to_text(audio_file)
    response_text = get_openai_response(text)
    audio_response = text_to_audio(response_text)
    return audio_response

def start_recording(filename='recording.wav', duration=10, samplerate=44100):
    print("Recording started...")
    recording = []
    def callback(indata, frames, time, status):
        recording.append(indata.copy())

    with sd.InputStream(callback=callback, channels=1, samplerate=samplerate):
        time.sleep(duration)
    
    audio_data = np.concatenate(recording, axis=0)
    audio_segment = AudioSegment(
        audio_data.tobytes(), 
        frame_rate=samplerate,
        sample_width=audio_data.dtype.itemsize,
        channels=1
    )
    audio_segment.export(filename, format='wav')
    print("Recording saved as:", filename)

def stop_recording():
    pass
