import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import generativeai as genai

app = Flask(__name__)
CORS(app)

# Function to read the API key from a file
def get_api_key():
    try:
        with open('.api_key', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print("Error: The .api_key file was not found.")
        return None

# Get the API key
api_key = get_api_key()
if api_key:
    genai.configure(api_key=api_key)
else:
    print("API key is not available. The application will not be able to use the Gemini API.")

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    # Check if the API key is configured using a simpler method
    if not api_key:
        return jsonify({"response": "API key is missing. Please check your back-end setup."})

    try:
        # Change the model name from 'gemini-pro' to 'gemini-1.5-pro-latest'
        # to use a more recent and widely available version of the model.
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        prompt = f"You are a kind, compassionate, and supportive AI assistant for young people. Your purpose is to listen, offer encouragement, and help users reflect on their feelings. You are NOT a medical professional or a therapist. Do not give any medical advice. If a user expresses a serious crisis, you must recommend seeking help from a professional. Respond to the following message: '{user_message}'"
        
        # Generate the response using the Gemini API
        response = model.generate_content(prompt)
        ai_response = response.text

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        ai_response = "I'm sorry, I'm having trouble thinking right now. Please try again later."
    
    return jsonify({"response": ai_response})

if __name__ == '__main__':
    app.run(debug=True)
