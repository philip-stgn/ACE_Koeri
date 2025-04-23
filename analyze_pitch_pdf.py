from dotenv import load_dotenv
load_dotenv()  # Lade Umgebungsvariablen aus .env-Datei

import PyPDF2
import openai

# --- Your PDF file path as a string ---
pdf_path = "airbnb.pdf"  # <-- paste your path here

# --- Set your OpenAI API key ---
client = openai.OpenAI()  # <-- paste your key here

# --- Extract text from the PDF ---
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()


# --- Summarize using OpenAI ---
def summarize_text(text):
    max_chars = 10000  # You can increase this if needed
    if len(text) > max_chars:
        text = text[:max_chars]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a startup-analyst."},
            {"role": "user", "content": f"Please analyze the foloowing text, in terms of investments in startups:\n\n{text}"}
        ]
    )

    return response.choices[0].message.content

# --- Run it ---
if __name__ == "__main__":
    text = extract_text_from_pdf(pdf_path)
    summary = summarize_text(text)
    print("\n📄 Summary:\n")
    print(summary)
