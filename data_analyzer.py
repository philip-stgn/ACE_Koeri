import os
import openai
import csv
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def read_csv(file_path):
    """Reads the content of a CSV file and returns it as a string."""
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        csv_content = "\n".join([", ".join(row) for row in reader])
    return csv_content

def send_to_ai(prompt, csv_content):
    """Sends the CSV content to the AI model with the given prompt."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{prompt}\n\n{csv_content}"}
        ]
    )
    return response['choices'][0]['message']['content']

def main():
    # Input CSV file path
    csv_file_path = input("/Users/torbeng/Documents/code/qhack/ACE_Koeri/INSERT")
    
    # Read the CSV content
    csv_content = read_csv(csv_file_path)
    
    # Prompt for the AI
    prompt = input("")
    
    # Send the CSV content to the AI
    try:
        ai_response = send_to_ai(prompt, csv_content)
        output_file_path = "/Users/torbeng/Documents/code/qhack/ACE_Koeri/ai_response.txt"
        with open(output_file_path, mode='w') as output_file:
            output_file.write("AI Response:\n")
            output_file.write(ai_response)
        print(f"AI response has been written to {output_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()