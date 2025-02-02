from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Load the dataset
df = pd.read_csv('./dataSets/corrected_mental_health_questions.csv')

# Endpoint to fetch a random question with options
@app.route('/get-question/<int:question_id>', methods=['GET'])
def get_question(question_id):
    # Fetch question by Question ID
    question_rows = df[df['Question_id'] == question_id]

    if question_rows.empty:
        return jsonify({"error": "Question not found"}), 404

    question_text = question_rows.iloc[0]['Question']

    options = []
    for idx, (_, row) in enumerate(question_rows.iterrows()):
        if idx < 4:  # Include up to 4 options
            options.append({
                "id": idx + 1,
                "text": row['Option_name'],
                "feeling": row['Feeling'],
                "score": row['Score']
            })

    return jsonify({
        "question_id": question_id,
        "question": question_text,
        "options": options
    })

# Endpoint to submit the quiz and calculate score
@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    user_answers = request.json.get('answers', {})  # Example: {"1": 1, "2": 3}

    total_score = 0
    for question_id, selected_option in user_answers.items():
        question_rows = df[df['Question_id'] == int(question_id)]

        if not question_rows.empty:
            selected_row = question_rows.iloc[selected_option - 1]  # Match index with option ID
            total_score += selected_row['Score']

    return jsonify({
        "score": total_score,
        "total_questions": len(user_answers)
    })

if __name__ == '__main__':
    app.run(debug=True)
