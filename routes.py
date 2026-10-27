from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, QuizResult
import pandas as pd
import os

# Define the Blueprint
main_routes = Blueprint('main_routes', __name__)
chat_routes = Blueprint('chat_routes', __name__)
mindful_activities = Blueprint('mindful_activities', __name__)

# Load the dataset
df_path = os.path.join(os.path.dirname(__file__), 'DataSets', 'corrected_mental_health_questions.csv')
df = pd.read_csv(df_path)

# Validate dataset columns
expected_columns = ['Question_id', 'Question', 'Option_name', 'Feeling', 'Score']
if not all(col in df.columns for col in expected_columns):
    raise ValueError(f"Dataset missing required columns: {expected_columns}")

@main_routes.route('/')
def index():
    return render_template('index.html')

@mindful_activities.route('/breathing')
def breathing():
    return render_template('breathing.html')

@mindful_activities.route('/nature-walk')
def nature_walk():
    return render_template('nature_walk.html')

@mindful_activities.route('/journaling')
def journaling():
    return render_template('journaling.html')

@mindful_activities.route('/calming-music')
def calming_music():
    return render_template('calming_music.html')

############### Creating new Account ##################
@main_routes.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists.', 'danger')
            return redirect(url_for('main_routes.register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('main_routes.login'))

    return render_template('signup.html')

################### Login in Existing Account ##################
@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main_routes.dashboard'))

        flash('Invalid credentials. Please try again.', 'danger')
        return redirect(url_for('main_routes.login'))

    return render_template('login.html')

@main_routes.route('/blog')
def blog():
    return render_template('blog.html')

@main_routes.route('/about')
def about():
    return render_template('about.html')

@main_routes.route('/contact', methods=['POST'])
def contact():
    flash('Thank you for your message! We will get back to you soon.', 'success')
    return redirect(url_for('main_routes.index'))

@main_routes.route('/result')
@login_required
def result():
    return render_template('resultPage.html')

@main_routes.route('/dashboard')
@login_required
def dashboard():
    history = QuizResult.query.filter_by(user_id=current_user.id).order_by(QuizResult.date.desc()).all()
    return render_template('dashboard.html', history=history)


########### Logout from logged account #############
@main_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main_routes.login'))

# @main_routes.route('/quiz')
# @login_required
@main_routes.route('/quiz')
def quiz():
    if current_user.is_authenticated:
        return render_template('quiz.html')
    else:
        flash('You need to log in first to access the quiz.', 'warning')
        return redirect(url_for('main_routes.login')) 

@main_routes.route('/chatbot')
@login_required
def chatbot():
    return render_template('chatbot.html')

@main_routes.route('/start-quiz')
def start_quiz():
    # Get 10 random unique question strings
    unique_questions = df['Question'].unique()
    import random
    selected_questions = random.sample(list(unique_questions), min(10, len(unique_questions)))
    
    # Get one Question_id for each selected question string
    question_ids = []
    for q_text in selected_questions:
        q_id = df[df['Question'] == q_text]['Question_id'].iloc[0]
        question_ids.append(int(q_id))
    
    return jsonify({"question_ids": question_ids})

# Endpoint to fetch a question with options
@main_routes.route('/get-question/<int:question_id>', methods=['GET'])
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
@main_routes.route('/submit-quiz', methods=['POST'])
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

    max_possible_score = 0
    for question_id in user_answers.keys():
        question_rows = df[df['Question_id'] == int(question_id)]
        if not question_rows.empty:
            max_possible_score += question_rows['Score'].max()

    if max_possible_score == 0: max_possible_score = 1
    scaled_score = round((total_score / max_possible_score) * 10)

    if current_user.is_authenticated:
        result = QuizResult(score=scaled_score, user_id=current_user.id)
        db.session.add(result)
        db.session.commit()

    return jsonify({
        "score": scaled_score,
        "total_questions": len(user_answers)
    })
