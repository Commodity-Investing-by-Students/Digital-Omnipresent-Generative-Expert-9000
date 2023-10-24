import torch
import torchaudio
import torch.nn as nn
import torch.nn.functional as F
import os
import sys
import IPython

tortoise_tts_fast_dir =r"C:\Users\mcovi\source\repos\Glados-tts\tortoise-tts-fast"
sys.path.insert(0, tortoise_tts_fast_dir)

from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio, load_voice, load_voices

def setup():

    CUSTOM_VOICE_NAME = "glados"
    custom_voice_folder = f"tortoise-tts-fast\tortoise\voices\{CUSTOM_VOICE_NAME}"

    if not os.path.exists(custom_voice_folder):
        os.makedirs(custom_voice_folder)
    os.chdir(custom_voice_folder)
    return CUSTOM_VOICE_NAME

def main():

    tts = TextToSpeech()
    CUSTOM_VOICE_NAME = setup()
    text = "Hello, I am the digital omnipresent generative expert 9000.  Please call me DOGE."
    #input("Input Text Voice: ")
    preset = "ultra_fast"

    #tts = TextToSpeech(use_deepspeed=True, kv_cache=True)
    voice_samples, conditioning_latents = load_voice(CUSTOM_VOICE_NAME)

    print(voice_samples)
    print(conditioning_latents)

    #gen = tts.tts_with_preset(text, voice_samples=voice_samples, conditioning_latents=conditioning_latents,preset=preset)
    gen = tts.tts_with_preset(text, voice_samples=voice_samples, conditioning_latents=conditioning_latents, preset="single_sample", candidates=1)

    torchaudio.save(f'generated-{CUSTOM_VOICE_NAME}.wav', gen.squeeze(0).cpu(), 24000)
    IPython.display.Audio(f'generated-{CUSTOM_VOICE_NAME}.wav')