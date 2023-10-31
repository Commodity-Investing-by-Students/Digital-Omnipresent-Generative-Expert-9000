import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import keyboard
import time
import sys
import whisper
from playsound import playsound

sys.path.append(r'C:\Users\mcovi\source\repos\Glados-tts')
sys.path.append(r'C:\Users\mcovi\source\repos\Glados-tts\glados-tts')

from glados import tts_runner

fs = 44100  # Sample rate
channels = 2  # Number of audio channels

print("Press the spacebar to start recording")
keyboard.wait('space')
print("Recording... Press the spacebar again to stop")

audio = []
with sd.InputStream(samplerate=fs, channels=channels) as stream:
    while True:
        frame, overflowed = stream.read(fs // 10)       
        audio.append(frame)
        if keyboard.is_pressed('space'):
            print("Recording stopped")
            break
audio = np.concatenate(audio, axis=0)
audio = np.int16(audio * np.iinfo(np.int16).max)

inputFile = 'input_voice.wav'
write(inputFile , fs, audio)
print("Finished recording. The audio is saved as 'input_voice.wav'")      

model = whisper.load_model('base.en')
option = whisper.DecodingOptions(fp16=False)
result = model.transcribe('input_voice.wav')

glados_engine = tts_runner(use_p1=True, log=True)
text = (result['text'])  
glados_engine.speak(text, save=True)  
playsound(r'C:\Users\mcovi\source\repos\Glados-tts\output.wav')

    
