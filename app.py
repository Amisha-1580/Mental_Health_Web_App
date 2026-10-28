from flask import Flask
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from models import db, bcrypt, login_manager
from routes import main_routes, mindful_activities, chat_api
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ── Secret key ────────────────────────────────────────────────────────────────
secret_key = os.getenv('SECRET_KEY')
if not secret_key:
    raise RuntimeError(
        "SECRET_KEY environment variable is not set. "
        "Add a strong random value to your .env file."
    )
app.config['SECRET_KEY'] = secret_key

# ── Database ───────────────────────────────────────────────────────────────────
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ── CSRF protection ───────────────────────────────────────────────────────────
csrf = CSRFProtect(app)
# The /submit-quiz and chatbot endpoints are called via fetch() with JSON bodies.
# Flask-WTF skips CSRF for requests whose Content-Type is application/json when
# WTF_CSRF_CHECK_DEFAULT is True, but we explicitly exempt them to be explicit.
csrf.exempt('routes.main_routes.submit_quiz')
csrf.exempt(chat_api)
csrf.exempt(mindful_activities)

# ── CORS ───────────────────────────────────────────────────────────────────────
CORS(app, resources={
    r"/get-question/*": {"origins": "*"},
    r"/get-answer/*":   {"origins": "*"},
    r"/chat/*":         {"origins": "*"},
})

# ── Extensions ─────────────────────────────────────────────────────────────────
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()

# ── Blueprints ─────────────────────────────────────────────────────────────────
app.register_blueprint(main_routes,       url_prefix='/')
app.register_blueprint(mindful_activities, url_prefix='/mindful-activities')

# ── Run ────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
