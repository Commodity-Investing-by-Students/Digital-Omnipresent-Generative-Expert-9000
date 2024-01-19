#import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
#import keyboard
import time
import sys
#import whisper
#from playsound import playsound

sys.path.append(r'C:\Users\mcovi\source\repos\Glados-tts')
sys.path.append(r'C:\Users\mcovi\source\repos\Glados-tts\glados-tts')
sys.path.append(r'C:\Users\mcovi\source\repos\sounds')

from glados import TTSRunner


def speak(text):
    glados_engine = TTSRunner(use_p1=True, log=True) 
    glados_engine.speak(text, save=True)  

    # Wait for all audio to be played before returning
    while not glados_engine.queue.empty() or glados_engine.playing:
        time.sleep(0.1)

    print("Finished Speaking.")
    
# need to pronounce eigh eye or artifical intelligence not AI , DOGE-9000 to DOGE 9000, 
    
def main(): 

    #text = input("Text: ")
    #speak(text)
    #input_text = listen()
    #print(input_text)

    speak(sys.argv[1])

  
if __name__=="__main__": 
    main() 