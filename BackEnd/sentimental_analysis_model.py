import pandas as pd
from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from flask_cors import CORS
CORS(sentimental_analysis_model)

app = Flask(__name__)

# Load the trained model
model = MultinomialNB()
model.load("mental_health_model.pkl")

# Load the vectorizer
vectorizer = CountVectorizer()
vectorizer.load("mental_health_vectorizer.pkl")

# Load the tokenizer
tokenizer = CountVectorizer().build_tokenizer()

# Load the trained model
model = MultinomialNB()

# Predefined questions and answers
predefined_qna = {
    "What is mental health?": "Mental health includes emotional, psychological, and social well-being. It affects how we think, feel, and behave.",
    "How can I improve my mental health?": "Engage in regular exercise, maintain a healthy diet, seek support from loved ones, and consider therapy if needed.",
    "What is depression?": "Depression is a common mental health disorder characterized by persistent sadness and loss of interest in activities.",
    "How can I manage anxiety?": "Practice mindfulness, deep breathing exercises, and seek professional help if anxiety interferes with daily life.",
}

# Load datasets


sentiment_dataset_path = "./DataSets/mental_health_sentiment_dataset.csv"  # Replace with the actual path
tips_dataset_path = "./DataSets/mental_health_conditions.csv"  # Replace with the actual path

# Load sentiment dataset
try:
    sentiment_data = pd.read_csv(sentiment_dataset_path)
except FileNotFoundError:
    raise FileNotFoundError(f"Sentiment dataset not found at {sentiment_dataset_path}")

# Load tips dataset
try:
    tips_data = pd.read_csv(tips_dataset_path)
except FileNotFoundError:
    raise FileNotFoundError(f"Tips dataset not found at {tips_dataset_path}")

# Check for and handle NaN values
if sentiment_data.isna().sum().any():
    print("Missing values found. Cleaning the data...")
    sentiment_data["query"].fillna("", inplace=True)
    sentiment_data["condition"].fillna("Unknown", inplace=True)
    sentiment_data["sentiment"].fillna("neutral", inplace=True)

# Train a basic sentiment and condition classifier
X = sentiment_data["query"]
y_condition = sentiment_data["condition"]
y_sentiment = sentiment_data["sentiment"]

# Create a pipeline for the classifier
condition_model = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('classifier', MultinomialNB())
])

sentiment_model = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('classifier', MultinomialNB())
])

condition_model.fit(X, y_condition)
sentiment_model.fit(X, y_sentiment)

# Initialize Flask app
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("query", "")
    
    if not user_input:
        return jsonify({"error": "Query is required"}), 400
    
    # Check predefined questions
    predefined_answer = predefined_qna.get(user_input)
    if predefined_answer:
        return jsonify({
            "query": user_input,
            "answer": predefined_answer
        })
    
    # Predict mental health condition and sentiment
    predicted_condition = condition_model.predict([user_input])[0]
    predicted_sentiment = sentiment_model.predict([user_input])[0]
    
    # Fetch tips and treatments
    tips = tips_data[tips_data["Mental Health Condition"] == predicted_condition]["Treatments and Tips"].values
    tips_response = tips[0] if len(tips) > 0 else "No specific tips available for the identified condition."
    
    response = {
        "query": user_input,
        "condition": predicted_condition,
        "sentiment": predicted_sentiment,
        "tips": tips_response
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)


