from pydub import AudioSegment
import sys

sys.path.append(r'C:\Users\mcovi\source\repos\Glados-tts\sounds')

def increase_volume(input_file, output_file, gain_in_db):
    try:
        # Load the audio file
        audio = AudioSegment.from_file(input_file, format="mp3")

        # Increase the volume by the specified gain (in dB)
        audio = audio + gain_in_db

        # Export the modified audio to a new file
        audio.export(output_file, format="mp3")
        
        print(f"Volume increased by {gain_in_db} dB and saved to {output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    input_file = r"C:\Users\mcovi\source\repos\Glados-tts\sounds\system_activate.mp3"   # Replace with your input file path
    output_file = "system_activate.mp3"  # Replace with your desired output file path
    gain_in_db = 10  # Adjust this value to change the volume (in dB)

    increase_volume(input_file, output_file, gain_in_db)
