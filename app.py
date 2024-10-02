from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Odczytujemy klucz API OpenAI z zmiennej środowiskowej
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('input')  # Używamy .get() dla bezpieczeństwa
    print(f"Received input: {user_input}")

    try:
        # Przygotowanie do wywołania OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Użyj właściwego modelu
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},  # Prompt systemowy
                {"role": "user", "content": user_input}  # Prompt użytkownika
            ]
        )

        # Wyciąganie odpowiedzi
        assistant_reply = response['choices'][0]['message']['content']
        print(f"Assistant reply: {assistant_reply}")

        return jsonify({"response": assistant_reply})

    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return jsonify({"error": "Wystąpił błąd w połączeniu z API OpenAI."}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Wystąpił nieoczekiwany błąd."}), 500

if __name__ == '__main__':
    app.run(debug=True)
