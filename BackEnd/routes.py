from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
import pandas as pd
import os

# Define the Blueprint
routes = Blueprint('routes', __name__)

# Load the dataset
df_path = os.path.join(os.path.dirname(__file__), 'DataSets', 'corrected_mental_health_questions.csv')
df = pd.read_csv(df_path)

# Validate dataset columns
expected_columns = ['Question_id', 'Question', 'Option_name', 'Feeling', 'Score']
if not all(col in df.columns for col in expected_columns):
    raise ValueError(f"Dataset missing required columns: {expected_columns}")

@routes.route('/')
def index():
    return render_template('index.html')

############### Creating new Account ##################
@routes.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists.', 'danger')
            return redirect(url_for('routes.register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('routes.login'))

    return render_template('signup.html')

################### Login in Existing Account ##################
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('routes.index'))

        flash('Invalid credentials. Please try again.', 'danger')
        return redirect(url_for('routes.login'))

    return render_template('login.html')

########### Logout from logged account #############
@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('routes.login'))

# @routes.route('/quiz')
# @login_required
@routes.route('/quiz')
def quiz():
    if current_user.is_authenticated:
        return render_template('quiz.html')
    else:
        flash('You need to log in first to access the quiz.', 'warning')
        return redirect(url_for('routes.login')) 

@routes.route('/chatbot')
@login_required
def chatbot():
    return render_template('chatbot.html')

# Endpoint to fetch a question with options
@routes.route('/get-question/<int:question_id>', methods=['GET'])
def get_question(question_id):
    question_rows = df[df['Question_id'] == question_id]
    if question_rows.empty:
        return jsonify({"error": "Question not found"}), 404

    question_text = question_rows.iloc[0]['Question']
    options = [
        {
            "id": idx + 1,
            "text": row['Option_name'],
            "feeling": row['Feeling'],
            "score": row['Score']
        }
        for idx, (_, row) in enumerate(question_rows.iterrows())
    ]

    return jsonify({
        "question_id": question_id,
        "question": question_text,
        "options": options
    })

# Endpoint to submit the quiz and calculate total score
@routes.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    user_answers = request.json.get('answers', {})  # Example: {"1": 1, "2": 3}
    total_score = 0

    for question_id, selected_option in user_answers.items():
        question_rows = df[df['Question_id'] == int(question_id)]
        if not question_rows.empty:
            selected_row = question_rows.iloc[selected_option - 1]
            total_score += selected_row['Score']
        else:
            return jsonify({"error": f"Question ID {question_id} not found"}), 400

    max_possible_score = len(user_answers) * 3  # Adjust based on actual data
    scaled_score = round((total_score / max_possible_score) * 10)

    return jsonify({
        "score": scaled_score,
        "total_questions": len(user_answers)
    })
