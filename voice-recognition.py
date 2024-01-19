import pyaudio
import wave
import audioop
import whisper

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
SILENCE_THRESHOLD = 20  # Adjust based on your microphone sensitivity
SILENCE_DURATION = 2.0  # 2 seconds of silence

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Placeholder function for detecting the activation phrase
def detect_activation_phrase(audio_data):
    # Implement your function or use Whisper here
    # Return True if "system activate" is detected
    return False

# Record audio in 5-second intervals and check for activation phrase
def listen_for_activation():
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Listening for activation phrase...")
    while True:
        frames = []
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

            if detect_activation_phrase(b''.join(frames)):
                print("Activation phrase detected!")
                stream.stop_stream()
                return record_after_activation()

    stream.close()

# Record until 2 seconds of silence
def record_after_activation():
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")
    frames = []
    silence_start = None

    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        # Detect silence in the audio stream
        if audioop.rms(data, 2) < SILENCE_THRESHOLD:
            if silence_start is None:
                silence_start = audio.get_stream_time()
            elif audio.get_stream_time() - silence_start > SILENCE_DURATION:
                print("Silence detected, stopping recording.")
                break
        else:
            silence_start = None

    stream.stop_stream()
    stream.close()

    # Save the recording to a file
    wf = wave.open('output.mp3', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return 'output.mp3'

if __name__ == '__main__':
    listen_for_activation()
