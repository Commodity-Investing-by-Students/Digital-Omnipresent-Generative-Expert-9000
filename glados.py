import torch
import numpy as np
from utils.tools import prepare_text
from scipy.io.wavfile import write
import time
import tempfile
import subprocess
from pydub import AudioSegment
from nltk import download
from nltk.tokenize import sent_tokenize
from sys import modules as mod
import threading
import pygame
import queue
import os

try:
    import winsound
except ImportError:
    from subprocess import call

print("Initializing TTS Engine...")

kwargs = {
    'stdout': subprocess.PIPE,
    'stderr': subprocess.PIPE,
    'stdin': subprocess.PIPE
}

class TTSRunner:
    def __init__(self, use_p1: bool = False, log: bool = False):
        self.log = log
        self.playing = False
        self.queue = queue.Queue()
        self.output_dir = "output_files"
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        if use_p1:
            self.emb = torch.load(
                r'C:\Users\mcovi\source\repos\Glados-tts\glados-tts\models\emb\glados_p1.pt')
        else:
            self.emb = torch.load(
                r'C:\Users\mcovi\source\repos\Glados-tts\glados-tts\models\emb\glados_p1.pt')

        if torch.cuda.is_available():
            self.device = 'cuda'
        elif torch.is_vulkan_available():
            self.device = 'vulkan'
        else:
            self.device = 'cpu'

        self.glados = torch.jit.load(
            r'C:\Users\mcovi\source\repos\Glados-tts\glados-tts\models/glados-new.pt')
        self.vocoder = torch.jit.load(
            r'C:\Users\mcovi\source\repos\Glados-tts\glados-tts\models/vocoder-gpu.pt', map_location=self.device)
        for i in range(2):
            init = self.glados.generate_jit(
                prepare_text(str(i)), self.emb, 1.0)
            init_mel = init['mel_post'].to(self.device)
            init_vo = self.vocoder(init_mel)

    def run_tts(self, text, alpha: float = 1.0) -> str:
        x = prepare_text(text)
        output_name = os.path.join(
            self.output_dir, f"output_{int(time.time())}.wav")

        with torch.no_grad():
            old_time = time.time()
            tts_output = self.glados.generate_jit(x, self.emb, alpha)
            if self.log:
                print("Forward Tacotron took " + str(
                    (time.time() - old_time) * 1000) + "ms")

            old_time = time.time()
            mel = tts_output['mel_post'].to(self.device)
            audio = self.vocoder(mel)
            if self.log:
                print("HiFiGAN took " + str(
                    (time.time() - old_time) * 1000) + "ms")

            audio = audio.squeeze()
            audio = audio * 32768.0
            audio = audio.cpu().numpy().astype('int16')

            write(output_name, 22050, audio)

        return output_name

    def speak_one_line(self, audio_path, name: str):

        #pygame.mixer.quit()
        #pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)
        try:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.delay(100)
        except pygame.error as e:
            print(f"Error while playing audio {name}: {str(e)}")

    def play_audio_thread(self):

        while True:
            if not self.queue.empty():
                audio_path, output_name = self.queue.get()
                self.playing = True
                try:
                    self.speak_one_line(audio_path, output_name)
                except pygame.error as e:
                    print(f"Error while playing audio: {str(e)}")
                self.playing = False

    def speak(self, text, alpha: float = 1.0, save: bool = False, delay: float = 10):
        download('punkt', quiet=self.log)
        sentences = sent_tokenize(text, language="english")

        playback_thread = threading.Thread(target=self.play_audio_thread)
        playback_thread.daemon = True
        playback_thread.start()

        for idx, sentence in enumerate(sentences):
            audio_path = self.run_tts(sentence)
            output_name = f"output{idx + 1}.wav"
            self.queue.put((audio_path, output_name))


if __name__ == "__main__":

    glados = TTSRunner(False, True)

    while(1==1):
        
        text = input("Input: ")

        if len(text) > 0:
            glados.speak(text, True)

        while not glados.queue.empty() or glados.playing:
            time.sleep(0.1)
