import re
import os
from openai import OpenAI

# Replace 'your_api_key_here' with your actual OpenAI API key
client = OpenAI(api_key='x')
max_tokens = 2000

def partition_text(text, max_length=max_tokens):
    """
    Partition the text into chunks based on punctuation, ensuring each chunk is under max_length tokens.
    """
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = []

    for sentence in sentences:
        if len(' '.join(current_chunk) + ' ' + sentence) > max_length:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
        else:
            current_chunk.append(sentence)
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

def process_text_with_prompt(text, prompt, step):
    """
    Process the given text with the specified LLM prompt and write the output to a file.
    """
    chunks = partition_text(text)
    processed_text = ""

    for chunk in chunks:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{
                "role": "system",
                "content": prompt
            }, {
                "role": "user",
                "content": chunk
            }],
            temperature=0.3,
            max_tokens=max_tokens
        )
        processed_text += response.choices[0].message.content.strip() + " "
    
    output_filename = f"{step}_output.txt"
    with open(output_filename, 'a+', encoding='utf-8') as file:
        print("response batch：\n\n")
        print(processed_text)
        file.write(processed_text)
    return output_filename

def main():
    # Load the initial text from a file specified by the user
    file_path = input("Please enter the file path to the txt file: ")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            initial_text = file.read()
    except Exception as e:
        print(f"An error occurred while trying to read the file: {e}")
        return

    # Define the series of prompts for transformations
    prompts = [
        "Please reformat and clean this text file to be more logically coherent.\
        Aim to omit as little as possible.\
        1) Do NOT artificially add any endings.\
        2) Do NOT include any explanatory introduction about what you're about to do.\
        3) If possible, clarify the speaker's name who is talking.",
        "Edit this to be a deepdive article.",
        "Add any necessary markdown and fix any grammatical errors."
    ]

    current_text_file = file_path

    for step, prompt in enumerate(prompts, start=1):
        print(f"Processing step {step}...")
        with open(current_text_file, 'r', encoding='utf-8') as file:
            current_text = file.read()
        
        current_text_file = process_text_with_prompt(current_text, prompt, step)
        print(f"Output written to {current_text_file}")

if __name__ == "__main__":
    main()