from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Load the dataset
df = pd.read_csv('./dataSets/corrected_mental_health_questions.csv')

# Endpoint to fetch a question with options
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
                "score": row['Score']  # Each option has a score
            })

    return jsonify({
        "question_id": question_id,
        "question": question_text,
        "options": options
    })

# Endpoint to submit the quiz and calculate total score
@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    user_answers = request.json.get('answers', {})  # Example: {"1": 1, "2": 3}

    total_score = 0
    for question_id, selected_option in user_answers.items():
        question_rows = df[df['Question_id'] == int(question_id)]

        if not question_rows.empty:
            selected_row = question_rows.iloc[selected_option]  # Select based on index
            total_score += selected_row['Score']  # Sum up scores of chosen options

    # Scale score to be out of 10 (Assuming the max possible score isn't exactly 10)
    max_possible_score = len(user_answers) * 3  # Adjust if needed based on dataset
    scaled_score = round((total_score / max_possible_score) * 10)

    return jsonify({
        "score": scaled_score,  # Scaled score out of 10
        "total_questions": len(user_answers)
    })

if __name__ == '__main__':
    app.run(debug=True)
