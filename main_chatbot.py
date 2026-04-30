from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from transformers import pipeline

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure OpenAI API
openai.api_key = "YOUR_OPENAI_API_KEY"

# Set up Hugging Face sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get user input
        user_input = request.json.get('message', '')

        if not user_input:
            return jsonify({"error": "Message is required."}), 400

        # Perform sentiment analysis
        sentiment = sentiment_pipeline(user_input)[0]
        sentiment_label = sentiment['label']
        sentiment_score = sentiment['score']

        # Create prompt for OpenAI API based on sentiment
        gpt_prompt = (
            f"User Query: {user_input}\n"
            f"Sentiment: {sentiment_label} ({sentiment_score})\n"
            "You are a mental health chatbot. Respond with empathy and provide mental health tips if needed."
        )

        # Get response from OpenAI GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a friendly mental health chatbot."},
                {"role": "user", "content": gpt_prompt}
            ]
        )

        bot_response = response.choices[0].message['content']

        # Return the response
        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
