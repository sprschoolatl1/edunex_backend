from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# API key MUST come from environment variable
API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route("/gemini", methods=["POST"])
def gemini_chat():
    data = request.get_json()
    user_msg = data.get("query", "")

    if not user_msg:
        return jsonify({"answer": "Please enter a question."})

    if not API_KEY:
        return jsonify({"answer": "API key not configured."}), 500

    url = (
    "https://generativelanguage.googleapis.com/v1/models/"
    "gemini-1.5-flash:generateContent?key=" + API_KEY
)


    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": (
                            "INSTRUCTION: Always give short answers (2–3 lines). "
                            "Give long explanations ONLY if the user says: "
                            "'explain in detail', 'long answer', or 'full explanation'.\n\n"
                            f"USER QUESTION: {user_msg}"
                        )
                    }
                ]
            }
        ]
    }

    try:
        r = requests.post(url, json=payload, timeout=15)
        r.raise_for_status()
        response = r.json()

        parts = response["candidates"][0]["content"]["parts"]
        text = "\n".join(p.get("text", "") for p in parts)

        return jsonify({"answer": text})

    except Exception as e:
        return jsonify({"answer": f"AI error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

