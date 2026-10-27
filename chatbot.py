from flask import jsonify, request, Blueprint
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

chat = Blueprint('chat', __name__)

# ── Gemini client ──────────────────────────────────────────────────────────────
_api_key = os.getenv("GEMINI_API_KEY")
if not _api_key:
    raise RuntimeError(
        "GEMINI_API_KEY environment variable is not set. "
        "Add it to your .env file."
    )
client = genai.Client(api_key=_api_key)

# Model: gemini-2.0-flash is the stable, GA release as of 2025.
# Update here when a newer stable model is available.
GEMINI_MODEL = "gemini-2.0-flash"

SYSTEM_PROMPT = """\
You are a kind, empathetic, human-like assistant.

When users talk about emotions or mental health:
- Respond warmly and naturally.
- Offer simple, practical coping ideas.
- Be supportive but clarify you are not a doctor.
- If the user shows crisis signs, gently suggest professional help.\
"""


@chat.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Server running"})


@chat.route("/chat", methods=["POST"])
def chat_route():
    try:
        data         = request.get_json(silent=True) or {}
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "Please provide a message."}), 400

        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_message}"

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=full_prompt,
        )

        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({
            "reply": "Sorry — something went wrong.",
            "error": str(e),
        }), 500