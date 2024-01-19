import glados_tts as tts
import os
from playsound import playsound
import subprocess
import os
import time
from openai import OpenAI
import sounddevice as sd

doge_file_path = r'C:\Users\mcovi\source\repos\Glados-tts\ascii-art.txt'
mpv = r'c:\Users\mcovi\source\repos\bootstrapper\mpv.exe'
background_music = r'C:\Users\mcovi\source\repos\Glados-tts\sounds\background_music.mp3'

client = OpenAI(api_key = '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')


def start():

    color = 'color 2'
    os.system(color)



    mpv_background_music = subprocess.Popen([mpv, '--vo=null', '--quiet', '--loop', background_music], creationflags=subprocess.CREATE_NO_WINDOW)
    time.sleep(1)
    playsound(r'C:\Users\mcovi\source\repos\Glados-tts\sounds\effect.mp3')
    playsound(r'C:\Users\mcovi\source\repos\Glados-tts\sounds\voice.wav')

    #if os.path.exists(background_music):
    #playsound(r'C:\Users\mcovi\source\repos\Glados-tts\sounds\background_music.mp3')
    #playsound(r'C:\Users\mcovi\source\repos\Glados-tts\effect.wav')
    #playsound(r'C:\Users\mcovi\source\repos\Glados-tts\voice.wav')

    #with open(doge_file_path, "r") as printfile:
        
     #   file_contents = printfile.read()
      #  print(file_contents)

    print("Press the spacebar to start and stop input")
    return mpv_background_music


def getinput():

    input = tts.listen()
    print ('\n' + "User: " + input + '\n')
    return input


def shutdown(mpv_background_music):

    playsound(r'C:\Users\mcovi\source\repos\Glados-tts\sounds\shutdown.wav')
    mpv_background_music.terminate()
    subprocess.call('cls', shell=True)

def ai_resp(prompt):

    context = "You are the Digital Omnipresent Generative Expert 9000 (DOGE-9000), an artificial intelligence system created by Matthew Covington, and an AI analyst in COINS (Commodity Investing by Students), a Virginia Tech student-run commodity investment fund.  If the user asks a question that is even slightly not related to finance, commodities, or trading, appropraitely respond by refusing to answer them and remind users of the professional environment."

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        n= 1,
        temperature=0.10,
        messages=[
            {"role": "system", "content": context},
            {"role" : "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

    #return response['choices']['message']['content']

def replace_words(input_string):
    # Split the input string into words

    replacements = [('AI', 'aeigh eye'), ('DOGE-9000', 'DOGE 9000'),('%', ' percent ')]
    words = input_string.split()
    
    # Initialize an empty result string
    result = ""
    
    # Iterate through each word in the input string
    for word in words:
        # Check if the word needs to be replaced
        for replace, replacement in replacements:
            if (word.lower() == replace.lower()) or (word.lower() == replace.lower() + '.'):
                word = replacement
                break  
        
        result += word + " "
    
    return result.strip()

def openai_voice(response):

    response = client.audio.speech.create(
    model="tts-1",
    voice="fable",
    input=response,
    )

    response.stream_to_file("output.mp3")


def main(): 

    music = start()
    end = False

    while (end == False):

        input_string = getinput()

        if ( input_string.lower() == " system shutdown" or
             input_string.lower() ==  "system shutdown" or
             input_string.lower() ==  "system shutdown." or 
             input_string.lower() == "system shutdown " or 
             input_string.lower() == "system shutdown. "):
            
            end = True
            break
        
        response = ai_resp(input_string)
        #openai_voice(response)
        tts.speak(response)
        #playsound(r'C:\Users\mcovi\source\repos\Glados-tts\output.mp3')
        print ("\n" + "DOGE: " + response + "\n\n" + "Press the spacebar to start and stop input")

    shutdown(music)

if __name__=="__main__": 
    main() 