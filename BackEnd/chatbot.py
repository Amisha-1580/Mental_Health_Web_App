import torch
from transformers import BertTokenizer, BertForSequenceClassification
from flask import Flask, request, jsonify
import numpy as np
import joblib  # For loading encoders

# Load the fine-tuned model and encoders
model = BertForSequenceClassification.from_pretrained('chatbot_model')
tokenizer = BertTokenizer.from_pretrained('chatbot_model')

# Load encoders after model
sentiment_encoder = joblib.load('sentiment_encoder.pkl')  # Load the pre-trained sentiment encoder
intent_encoder = joblib.load('intent_encoder.pkl')        # Load the pre-trained intent encoder
emotion_encoder = joblib.load('emotion_encoder.pkl')      # Load the pre-trained emotion encoder

# Flask app setup
app = Flask(_name_)

# Function to preprocess and predict sentiment, intent, and emotion
def predict(user_input):
    # Tokenize the input
    inputs = tokenizer.encode_plus(
        user_input,
        truncation=True,
        padding="max_length",
        max_length=128,
        return_tensors='pt'
    )

    # Model prediction
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits  # Output logits for each task

    # Assuming that logits contain sentiment, intent, and emotion predictions
    # Extract logits for sentiment, intent, and emotion
    sentiment_logits, intent_logits, emotion_logits = logits[0]

    # Get the predictions by selecting the class with the highest logit
    sentiment = sentiment_encoder.inverse_transform([torch.argmax(sentiment_logits).item()])[0]
    intent = intent_encoder.inverse_transform([torch.argmax(intent_logits).item()])[0]
    emotion = emotion_encoder.inverse_transform([torch.argmax(emotion_logits).item()])[0]

    return sentiment, intent, emotion

# Flask route for chatbot interaction
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('query', '')  # Get user input from request

    if not user_input:
        return jsonify({"error": "No query provided."}), 400

    # Get predictions for sentiment, intent, and emotion
    sentiment, intent, emotion = predict(user_input)

    # Generate tips based on sentiment
    if sentiment == 'positive':
        tips = "You're doing great! Keep up the good work."
    elif sentiment == 'negative':
        tips = "It seems you're feeling down. Take a moment for yourself. How about a short walk?"
    else:
        tips = "You're feeling neutral. It's always good to stay balanced."

    # Return the response with sentiment, intent, emotion, and tips
    return jsonify({
        "sentiment": sentiment,
        "intent": intent,
        "emotion": emotion,
        "tips": tips
    })

if _name_ == '_main_':
    app.run(debug=True)