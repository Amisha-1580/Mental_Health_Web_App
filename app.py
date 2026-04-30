from flask import Flask
from flask_cors import CORS
from models import db, bcrypt, login_manager
from routes import routes  # Import the Blueprint
from chatbot import chat  # Import the chatbot Blueprint
import os

app = Flask(__name__)
CORS(app, resources={r"/get-question/*": {"origins": "*"}})
CORS(app, resources={r"/get-answer/*": {"origins": "*"}})
CORS(app, resources={r"/chat/*": {"origins": "*"}})

# Connect to SQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = os.getenv('jwt_secret')  # Use the secret key from .env

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()

# Register the Blueprint
app.register_blueprint(routes, url_prefix='/')  # Use '/' as the prefix
app.register_blueprint(chat, url_prefix='/chat') 

# Run the app
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
