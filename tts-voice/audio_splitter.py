from pydub import AudioSegment
import os

# Function to split a .wav file into 8-second segments
def split_wav_into_segments(input_file, output_folder):
    audio = AudioSegment.from_file(input_file, format="wav")
    
    # Calculate the duration of each segment in milliseconds (8 seconds)
    segment_length_ms = 8000
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Split the audio into segments
    for i, start in enumerate(range(0, len(audio), segment_length_ms)):
        end = start + segment_length_ms
        segment = audio[start:end]
        output_file = os.path.join(output_folder, f'segment_{i + 1}.wav')
        segment.export(output_file, format="wav")
        print(f'Saved {output_file}')

# Input .wav file and output folder
input_wav_file = r"C:\Users\mcovi\source\repos\Glados-tts\glados_audio.wav"  # Replace with the path to your input .wav file
output_folder = r"C:\Users\mcovi\source\repos\Glados-tts\output_segments"  # Replace with the desired output folder name

# Call the function to split the .wav file
split_wav_into_segments(input_wav_file, output_folder)
