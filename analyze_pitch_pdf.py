from dotenv import load_dotenv
load_dotenv()  # Lade Umgebungsvariablen aus .env-Datei
import fitz  # PyMuPDF
import openai

# Deine OpenAI API-Schlüssel

def extract_text_from_pdf(pdf_path):
    """
    Extrahiert den Text aus einer PDF-Datei.
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)  # Lade die Seite
        text += page.get_text()  # Extrahiere den Text
    return text

def analyze_text_with_chatgpt(text):
    """
    Sendet den extrahierten Text an die ChatGPT API und analysiert ihn.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # Wähle das Modell aus, z.B. GPT-4
        messages=[
            {"role": "system", "content": "Du bist ein Startup-Analyst."},
            {"role": "user", "content": f"Bitte analysiere den folgenden Text aus einem Pitchdeck, gehe dabei insbesondere auf die Marketsize ein und gebe diese an:\n\n{text}"}
        ]
    )
    
    # Rückgabe der Antwort von ChatGPT
    return response['choices'][0]['message']['content']

def main(pdf_path):
    """
    Hauptfunktion, die den Text extrahiert und die Analyse startet.
    """
    # Schritt 1: Extrahiere den Text aus der PDF
    print(f"Extrahiere Text aus der PDF-Datei: {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    
    # Schritt 2: Analysiere den extrahierten Text mit ChatGPT
    print("Analysiere den extrahierten Text mit ChatGPT...")
    analysis_result = analyze_text_with_chatgpt(text)
    
    # Schritt 3: Ausgabe der Analyse
    print("Antwort von ChatGPT:")
    print(analysis_result)

# Beispiel-PDF-Datei (ersetze diesen Pfad mit dem Pfad zu deinem Pitchdeck)
pdf_path = "airbnb.pdf"  # Ersetze dies mit dem Pfad zu deinem PDF-Dokument

# Starte das Skript
if __name__ == "__main__":
    main(pdf_path)