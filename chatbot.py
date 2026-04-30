from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Create Gemini client once
client = genai.Client(api_key=os.getenv("API_KEY"))

# System instruction (assistant personality)
SYSTEM_PROMPT = """
You are a kind, empathetic, human-like assistant.

When users talk about emotions or mental health:
- Respond warmly and naturally.
- Offer simple, practical coping ideas.
- Be supportive but clarify you are not a doctor.
- If user shows crisis signs, gently suggest professional help.
"""

@app.route("/")
def home():
    return jsonify({"status": "Server running"})


@app.route("/chat", methods=["POST"])
def chat():

    try:
        user_message = request.json.get("message", "")

        # Combine system + user message properly
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_message}"

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )

        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        return jsonify({
            "reply": "Sorry — something went wrong.",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)















# import torch
# from transformers import BertTokenizer, BertForSequenceClassification
# from flask import Flask, request, jsonify
# import numpy as np
# import joblib  # For loading encoders

# # Load the fine-tuned model and encoders
# model = BertForSequenceClassification.from_pretrained('chatbot_model')
# tokenizer = BertTokenizer.from_pretrained('chatbot_model')

# # Load encoders after model
# sentiment_encoder = joblib.load('sentiment_encoder.pkl')  # Load the pre-trained sentiment encoder
# intent_encoder = joblib.load('intent_encoder.pkl')        # Load the pre-trained intent encoder
# emotion_encoder = joblib.load('emotion_encoder.pkl')      # Load the pre-trained emotion encoder

# # Flask app setup
# app = Flask(_name_)

# # Function to preprocess and predict sentiment, intent, and emotion
# def predict(user_input):
#     # Tokenize the input
#     inputs = tokenizer.encode_plus(
#         user_input,
#         truncation=True,
#         padding="max_length",
#         max_length=128,
#         return_tensors='pt'
#     )

#     # Model prediction
#     with torch.no_grad():
#         outputs = model(**inputs)
#         logits = outputs.logits  # Output logits for each task

#     # Assuming that logits contain sentiment, intent, and emotion predictions
#     # Extract logits for sentiment, intent, and emotion
#     sentiment_logits, intent_logits, emotion_logits = logits[0]

#     # Get the predictions by selecting the class with the highest logit
#     sentiment = sentiment_encoder.inverse_transform([torch.argmax(sentiment_logits).item()])[0]
#     intent = intent_encoder.inverse_transform([torch.argmax(intent_logits).item()])[0]
#     emotion = emotion_encoder.inverse_transform([torch.argmax(emotion_logits).item()])[0]

#     return sentiment, intent, emotion

# # Flask route for chatbot interaction
# @app.route('/chat', methods=['POST'])
# def chat():
#     data = request.get_json()
#     user_input = data.get('query', '')  # Get user input from request

#     if not user_input:
#         return jsonify({"error": "No query provided."}), 400

#     # Get predictions for sentiment, intent, and emotion
#     sentiment, intent, emotion = predict(user_input)

#     # Generate tips based on sentiment
#     if sentiment == 'positive':
#         tips = "You're doing great! Keep up the good work."
#     elif sentiment == 'negative':
#         tips = "It seems you're feeling down. Take a moment for yourself. How about a short walk?"
#     else:
#         tips = "You're feeling neutral. It's always good to stay balanced."

#     # Return the response with sentiment, intent, emotion, and tips
#     return jsonify({
#         "sentiment": sentiment,
#         "intent": intent,
#         "emotion": emotion,
#         "tips": tips
#     })

# if _name_ == '_main_':
#     app.run(debug=True)
