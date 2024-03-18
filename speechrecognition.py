import sounddevice as sd
import numpy as np
import speech_recognition as sr
import chatmacro
import chatbot
import speechify
from datetime import datetime

audio_buffer = []  # Initialize an empty audio buffer

def audio_callback(indata, frames, time, status):
    global audio_buffer
    
    # Calculate the RMS (Root Mean Square) value
    rms = np.sqrt(np.mean(indata ** 2))
    print(rms)
    # Define a threshold value to detect audio
    threshold = 0.04
    
    if rms > threshold:
        print("Audio detected from the application!")
        
        audio_data = (indata * 32767).astype(np.int16)
        audio_buffer.append(audio_data)  # Append new audio data to buffer
    else:
        if len(audio_buffer) > 0:
            audio_data = (indata * 32767).astype(np.int16)
            audio_buffer.append(audio_data)
            process_audio_buffer()

def process_audio_buffer():
    global audio_buffer
    
    stacked_audio = np.concatenate(audio_buffer)
    
    recognizer = sr.Recognizer()
    audio_source = sr.AudioData(stacked_audio.tobytes(), sample_rate=sample_rate, sample_width=2)
    
    try:
        now = str(datetime.now()).replace(":", "-").replace(".", "-")
        text = recognizer.recognize_google(audio_source)
        print("Recognized text:", text)
        chatmacro.chat("You: "+text)
        response = chatbot.send_message(text, now)
        response_length = len(response)
        if response_length > 150:
            chatmacro.chat("Roxy: "+response[:150])
            response = response[150:]
            response_length = len(response)
            while response_length > 150:
                chatmacro.chat(response[:150])
                response = response[150:]
                response_length = len(response)
            chatmacro.chat(response)
            speechify.sound(now)
        else:
            chatmacro.chat("Roxy: "+response)
            speechify.sound(now)
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
        chatmacro.chat("filtered")
    audio_buffer = []

# Set the audio input device to the desired application
list = ['CABLE Output (VB-Audio Virtual , MME','Microphone (High Definition Aud']

pick = int(input('Device: '))
device = list[pick]

# Set the audio parameters
sample_rate = 48000#16000#
duration = 1.2  # Duration of each audio callback in seconds

# Start recording audio
def record():
    with sd.InputStream(device=device, channels=1, callback=audio_callback,
                        samplerate=sample_rate, blocksize=int(sample_rate * duration)):
        print("Listening for audio...")
        input("Press Enter to stop...")

record()