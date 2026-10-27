from flask import jsonify, request, Blueprint
# from flask_cors import CORS
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

chat = Blueprint('chat', __name__)

# Configure Gemini
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# System instruction
SYSTEM_PROMPT = """
You are a kind, empathetic, human-like assistant.

When users talk about emotions or mental health:
- Respond warmly and naturally.
- Offer simple, practical coping ideas.
- Be supportive but clarify you are not a doctor.
- If user shows crisis signs, gently suggest professional help.
"""

@chat.route("/")
def home():
    return jsonify({"status": "Server running"})


@chat.route("/chat", methods=["POST"])
def chat_route():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"reply": "Please provide a message"}), 400

        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_message}"

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
        )

        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        return jsonify({
            "reply": "Sorry — something went wrong.",
            "error": str(e)
        }), 500