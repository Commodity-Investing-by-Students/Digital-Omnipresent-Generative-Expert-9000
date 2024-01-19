import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import keyboard
import time
import sys
import whisper
from playsound import playsound
import os as os
import subprocess

sys.path.append(r'C:\Users\mcovi\source\repos\Glados-tts')
sys.path.append(r'C:\Users\mcovi\source\repos\Glados-tts\glados-tts')
sys.path.append(r'C:\Users\mcovi\source\repos\sounds')

mpv = r'c:\Users\mcovi\source\repos\bootstrapper\mpv.exe'

from glados import TTSRunner

import speech_recognition as sr

def listen_for_activation_phrase():

    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening for 'system activate'...")

        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=5)

        try:
            text = recognizer.recognize_google(audio)

            if "system activate" in text.lower():
                print("Activation phrase detected!")
                return True

        except sr.UnknownValueError:
            print("Could not understand audio, trying again...")

        except sr.RequestError as e:
            print(f"Could not request results from the service; {e}")

        return False
    

def listen():

    print("System actived.")
    play_audio_non_blocking(r'C:\Users\mcovi\source\repos\Glados-tts\sounds\system_activate.mp3')

    silence_threshold = 2
    fs = 44100  
    channels = 2  
    silence_frames = int(silence_threshold * fs / (fs // 10))

    audio = []
    silence_counter = 0
    with sd.InputStream(samplerate=fs, channels=channels) as stream:
        while True:
            frame, overflowed = stream.read(fs // 10)
            audio.append(frame)

            # Check for silence in the current frame
            if is_silence(frame, threshold=0.01):
                silence_counter += 1
            else:
                silence_counter = 0

            # Stop recording if silence has lasted long enough
            if silence_counter >= silence_frames:
                break

    # Concatenate all audio frames and normalize
    play_audio_non_blocking(r'C:\Users\mcovi\source\repos\Glados-tts\sounds\message_heard.mp3')
    audio = np.concatenate(audio, axis=0)
    audio = np.int16(audio * np.iinfo(np.int16).max)

    # Save the audio to a file
    inputFile = 'input_voice.wav'
    write(inputFile, fs, audio)

    # Interpret the speech using the interpret_speech function
    voicetext = interpret_speech(inputFile)
    return voicetext


def interpret_speech(input_voice_file):
    
    model = whisper.load_model('base.en')
    option = whisper.DecodingOptions(fp16=False)
    result = model.transcribe(input_voice_file)
    voicetext = (result['text']) 
    return voicetext

def play_audio_non_blocking(audio_file):

    try:
        subprocess.Popen([mpv, '--vo=null', '--quiet', audio_file], creationflags=subprocess.CREATE_NO_WINDOW)
        #print(f"Playing the audio: {audio_file}")

    except Exception as e:
        print(f"Failed to play audio: {e}")

def is_silence(audio, threshold):
    return np.max(np.abs(audio)) < threshold


def voice_input():
    if listen_for_activation_phrase():
        transcribed_text = listen()
        return transcribed_text

if __name__ == "__main__":

    if listen_for_activation_phrase():
        transcribed_text = listen()
        print(transcribed_text)


"""
recognizer = sr.Recognizer()

while True:
    with sr.Microphone() as source:
        print("Listening for 'system activate'...")
        
        # Adjust for ambient noise and record audio for 5 seconds
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=5)

    # Try to recognize the speech in the audio
    try:
        # Recognize speech using Google's speech recognition service
        text = recognizer.recognize_google(audio)

        # Check if the activation phrase is in the recognized text
        if "system activate" in text.lower():
            print("Activation phrase detected!")
            return True

    except sr.UnknownValueError:
        # If the audio isn't clear, delete the clip and continue
        print("Could not understand audio, trying again...")
        continue

    except sr.RequestError as e:
        # API was unreachable or unresponsive
        print(f"Could not request results from the service; {e}")

"""