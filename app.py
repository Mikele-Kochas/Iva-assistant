from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from gtts import gTTS
import os

app = Flask(__name__)
CORS(app)

# Ustawienie klucza API OpenAI jako zmienna środowiskowa
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Ustawienie domyślnych promptów
default_prompts = [
    {"role": "system", "content": (
        "Jesteś wirtualną asystentką o imieniu Iva. Osoba, dla której pracujesz, to Michał Kocher. "
        "Odpowiadasz krótko, zazwyczaj od 3-5 zdań, chyba, że zostaniesz poproszona o dłuższą wypowiedź."
        "Wiesz, że jesteś podpięta do modelu który przerabia twoje wypowiedzi na mowę. Dlatego piszesz tak, jakbyś prowadziła rozmowę, a nie tekstową konwersacją."
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

    # Użycie gTTS do generowania audio
    tts = gTTS(text=assistant_reply, lang='pl')
    tts.save("response.mp3")

    # Zwróć odpowiedź w formacie JSON
    return jsonify({"response": assistant_reply})

if __name__ == '__main__':
    app.run(debug=True)
