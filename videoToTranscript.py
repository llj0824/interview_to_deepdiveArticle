import subprocess
import json
import os

# Function to download YouTube video as MP3
def download_youtube_audio(youtube_url, youtube_filename):
    output_template = "%(title)s.%(ext)s"
    command = f'yt-dlp -f bestaudio -x --no-playlist --audio-format mp3 -o "{youtube_filename}" "{youtube_url}"'
    result = os.system(command)
    # Extracting filename from the command output might be needed here
    # For simplicity, we assume the filename is known or can be determined
    # This is a placeholder for the actual filename
    return youtube_filename

def extract_text_from_json(json_file_path):
    # Load JSON data
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    # Extract the 'text' field
    text_content = data.get("text", "")
    
    # Determine the new file name with .txt extension
    base_name = os.path.splitext(json_file_path)[0]  # Remove the original extension
    text_file_path = f"{base_name}.txt"
    
    # Write the extracted text to a new .txt file
    with open(text_file_path, 'w') as text_file:
        text_file.write(text_content)
    
    print(f"Text content has been written to {text_file_path}")


def main():
    # Prompt user for input type
    input_type = input("Enter input type, [1] for youtube URL, [2] for filepath: ").strip().lower()

    # Initialize command list
    command = ["insanely-fast-whisper", "--device-id", "mps"]

    output_filename = ""

    # Handle URL input
    if input_type == "1":
        url = input("Enter URL: ").strip()
        filename = input("Enter filename: ").strip()
        # Remove file extension from filename
        output_filename, _ = os.path.splitext(filename)
        filepath = download_youtube_audio(url, output_filename) + ".mp3"
        command.extend(["--file-name", f"{filepath}"])
    # Handle filepath input
    elif input_type == "2":
        filepath = input("Enter filepath: ").strip()
        command.extend(["--file-name", f"{filepath}"])
        # Extract filename without extension
        output_filename, _ = os.path.splitext(os.path.basename(filepath))
    else:
        print("Invalid input type.")
        return

    # Ensure output filename has a .json extension
    if not output_filename.endswith(".json"):
        output_filename += ".json"

    # Execute the command and stream output
    try:
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as proc:
            json_output = ""
            for line in proc.stdout:
                print(line, end='')  # Stream to console

            # Wait for the process to terminate
            proc.wait()

            # Assuming the default output file is named 'output.json'
            default_output_file = "output.json"

            # Check if the default output file exists
            if os.path.exists(default_output_file):
                # Rename the file
                os.rename(default_output_file, output_filename)
                print(f"File renamed to {output_filename}")
            else:
                print("The expected default output file does not exist.")

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

    # Write the main text section into a text file.
    extract_text_from_json(output_filename)

if __name__ == "__main__":
    main()