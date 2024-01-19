import streamlit as st
import time 
from PIL import Image
import glados_tts as tts
import os
from playsound import playsound
import subprocess
from openai import OpenAI
import sys
import shutil
import signal
import listen
import agent

OPEN_AI_KEY = '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'

doge_avatar = 'DogePDF.jpg'
icon = Image.open(doge_avatar)

doge_file_path = r'C:\Users\mcovi\source\repos\Glados-tts\ascii-art.txt'
mpv = r'c:\Users\mcovi\source\repos\bootstrapper\mpv.exe'
background_music = r'C:\Users\mcovi\source\repos\Glados-tts\sounds\background_music.mp3'

unidecode = r'C:\Users\mcovi\source\repos\Glados-tts\.venv\Lib\site-packages\unidecode'
sys.path.append(unidecode)

client = OpenAI(api_key = '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')


def start():

    mpv_background_music = subprocess.Popen([mpv, '--vo=null', '--quiet', '--loop', background_music], creationflags=subprocess.CREATE_NO_WINDOW)
    return mpv_background_music

def shutdown(mpv_background_music):

    playsound(r'C:\Users\mcovi\source\repos\Glados-tts\sounds\shutdown.wav')
    mpv_background_music.terminate()
    subprocess.call('cls', shell=True)

    with st.chat_message("assistant", avatar= '🐕'):

            assistant_response = 'Shutting down systems ... Complete.  Please close this window.'
            message_placeholder = st.empty()
            full_response = ""

            for chunk in assistant_response.split():
                full_response += chunk + " "

                time.sleep(0.05)

                if (chunk == 'Çomplete'):
                    time.sleep(1)

                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

    powershell_command = """
    Get-Process | Where-Object { $_.ProcessName -eq "mpv" } | ForEach-Object { Stop-Process -Id $_.Id }
    """
    try:
        subprocess.run(["powershell", "-Command", powershell_command], check=True)
        print("Successfully terminated 'mpv' processes.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to terminate 'mpv' processes: {e}")
        


def ai_resp(prompt):

    context = "You are the Digital Omnipresent Generative Expert 9000 (DOGE 9000), \
        an artificial intelligence system created by Matthew Covington, and an AI analyst \
        in COINS (which stand for Commodity Investing by Students), a Virginia Tech student-run commodity investment fund.\
        The purpose of COINS is to research and trade the exchange traded funds of commodities to generate alpha \
        or excess returns compared to the Bloomberg Commodity Index.  The funds are from the donations from the Virginia Tech foundation.  \
        Matthew Covington is a quant-research and generative AI analyst in the COINS quantitative division.  He did not create COINS nor is the master-mind behind it. \
        \
        You MUST mention Matthew Covington by name when talking about yourself.  Please answer in a narrative/story-like format.  Consider using hilarious analogies. \
        If the user asks a question that is not related \
        to finance, commodities, or trading, appropraitely respond by refusing to answer and remind users of the professional environment. \
        Finally, please chat in style of a urban youth, using slang like 'no cap', 'thats on my mama', 'finna', 'rizz', \
        'my guy', 'bruh', fire', 'hella', 'ass', 'shit', 'damn', 'lit', 'on god', \
        'sus', 'beefing', 'lowkey', 'highkey', 'for real', and 'dippin' in your response.  \
        Begin!"

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        n= 1,
        temperature=1.2,
        messages=[
            {"role": "system", "content": context},
            {"role" : "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content



def main():

    st.set_page_config(page_title="DOGE UI",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="collapsed"
    )


    st.title("DOGE-9000 User Interface 🐕 \t")        

    if "background_music" not in st.session_state:
        st.session_state.background_music = start() 
        subprocess.Popen([mpv, '--vo=null', '--quiet', r'C:\Users\mcovi\source\repos\Glados-tts\sounds\effect.mp3'], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen([mpv, '--vo=null', '--quiet', r'C:\Users\mcovi\source\repos\Glados-tts\sounds\voice.wav'], creationflags=subprocess.CREATE_NO_WINDOW)
    

    # Initialize session state for messages if not already present
    if "messages" not in st.session_state:

        st.session_state.messages = []

        
    if "doge" not in st.session_state:
        st.session_state.doge = agent.init()

    if "transcribed_text" not in st.session_state:
        st.session_state.transcribed_text = ""

    if "voice_activated" not in st.session_state:
        st.session_state.voice_activated = False

    prompt = st.chat_input("Say Something ...")

    if not st.session_state.voice_activated and not prompt:
        st.session_state.voice_activated = listen.listen_for_activation_phrase()

    if (st.session_state.voice_activated and not st.session_state.transcribed_text):
        st.session_state.transcribed_text = listen.listen()
        print(st.session_state.transcribed_text)

    if (st.session_state.voice_activated == 'shutdown'):

        shutdown(st.session_state.background_music)  
        st.session_state.background_music = None  

        directory_path = r'C:\Users\mcovi\source\repos\Glados-tts\output_files'

        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove file or link
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove directory and all its contents
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        
        st.stop()
        os.kill(os.getpid(), signal.SIGINT)

    processed_prompt = prompt or st.session_state.transcribed_text

       
    if (processed_prompt):

        if (processed_prompt.lower() == "system shutdown") or (processed_prompt.lower() == "system shutdown.") :
            shutdown(st.session_state.background_music)  
            st.session_state.background_music = None  

            directory_path = r'C:\Users\mcovi\source\repos\Glados-tts\output_files'

            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # Remove file or link
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Remove directory and all its contents
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
            
            st.stop()
            os.kill(os.getpid(), signal.SIGINT)

        st.empty()

        for message in st.session_state.messages:

                if message["role"] == "user":
                    avatar = "🤨"  
                elif message["role"] == "assistant":
                    avatar = "🐕"  
                else:
                    avatar = ""

                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])

                
        st.session_state.messages.append({"role": "user", "content": processed_prompt})

        with st.chat_message("user", avatar="🤨"):
            st.markdown(processed_prompt)

        assistant_response = agent.run(processed_prompt, st.session_state.doge)

        #assistant_response = ai_resp(processed_prompt)

        voice_tts = subprocess.Popen([ r'C:\Users\mcovi\source\repos\Glados-tts\.venv\Scripts\python.exe', r'C:\Users\mcovi\source\repos\Glados-tts\glados_tts.py', assistant_response], 
                                    env=os.environ, cwd=r'C:\Users\mcovi\source\repos\Glados-tts')
    
        time.sleep(10)

        with st.chat_message("assistant", avatar= '🐕'):

            message_placeholder = st.empty()
            full_response = ""
            chunks = assistant_response.split()
            print(f"There are " + str(len(chunks)) + " chunks")

            for i, chunk in enumerate(chunks):

                print("int i is on value " + str(i))

                full_response += chunk + " "
                time.sleep(0.20)

                if (i == len(chunks)-1):
                    message_placeholder.markdown(assistant_response.strip())
                    print("Final One!")
                else:
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(assistant_response.strip())


        st.session_state.messages.append({"role": "assistant", "content": full_response})

        st.session_state.voice_activated = False
        st.session_state.transcribed_text = ""
        processed_prompt = ""
        prompt = ""

    st.rerun()


    
if __name__ == "__main__":
    main()
