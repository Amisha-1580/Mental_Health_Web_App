from flask import Flask, request, jsonify
import tensorflow as tf
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

app = Flask(_name_)

# Load the trained model and vectorizer
model = tf.keras.models.load_model('Backend/model/mental_health_chatbot_model.h5')
vectorizer = joblib.load('Backend/model/vectorizer.pkl')
sentiment_encoder = joblib.load('Backend/model/sentiment_encoder.pkl')
intent_encoder = joblib.load('Backend/model/intent_encoder.pkl')
emotion_encoder = joblib.load('Backend/model/emotion_encoder.pkl')

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data['query']
    
    # Vectorize the user input
    user_input_vec = vectorizer.transform([user_input]).toarray()

    # Predict sentiment, intent, and emotion
    sentiment_pred = model.predict(user_input_vec)
    sentiment = sentiment_encoder.inverse_transform(np.argmax(sentiment_pred, axis=1))[0]

    # Example response based on sentiment (you can modify this as per your response generation logic)
    if sentiment == "Negative":
        response = "I'm sorry you're feeling that way. Try talking to a friend or taking a deep breath."
    else:
        response = "I'm glad you're doing well! Keep up the positive mindset."

    return jsonify({
        'condition': sentiment,
        'sentiment': sentiment,
        'tips': response
    })

if _name_ == "_main_":
    app.run(debug=True)