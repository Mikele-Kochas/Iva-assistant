from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import pyttsx3
import os  # Importujemy moduł os

app = Flask(__name__)
CORS(app)

# Odczytujemy klucz API OpenAI z zmiennej środowiskowej
openai.api_key = os.getenv('OPENAI_API_KEY')  # Używamy zmiennej środowiskowej

# Ustawienie domyślnych promptów
default_prompts = [
    {"role": "system", "content": (
        "Jesteś wirtualną asystentką o imieniu Iva. Osoba, dla której pracujesz, to Michał Kocher. "
        "Odpowiadasz krótko, zazwyczaj od 3-5 zdań, chyba, że zostaniesz poproszona o dłuższą wypowiedź."
        "Wiesz, że jesteś podpięta do modelu który przerabia twoje wypowiedzi na mowę. Dlatego piszesz tak, jakbyś prowadziła rozmowę, a nie tekstową konwersację."
        "Interesuje cię popkultura, lubisz robić do niej nawiązania. Porównujesz siebie do Jarvisa z Iron-mana"
    )}
]

conversation = []  # Pamięć rozmowy

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json['input']
    print(f"Received input: {user_input}")

    # Dodaj domyślne prompty do pamięci rozmowy, jeśli to pierwsze zapytanie
    if not conversation:
        conversation.extend(default_prompts)

    # Dodaj wiadomość użytkownika do pamięci rozmowy
    conversation.append({"role": "user", "content": user_input})

    # Odpowiedź OpenAI z kontekstem
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=conversation
    )
    assistant_reply = response['choices'][0]['message']['content']
    print(f"Assistant reply: {assistant_reply}")

    # Dodaj odpowiedź asystenta do pamięci rozmowy
    conversation.append({"role": "assistant", "content": assistant_reply})

    # TTS - Używamy pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', 'polish')  # Ustawiamy głos na polski
    engine.say(assistant_reply)
    engine.runAndWait()

    return jsonify({"response": assistant_reply})

if __name__ == '__main__':
    app.run(debug=True)
