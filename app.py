from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route("/")
def home():
    return "EduNex AI backend is running"

@app.route("/gemini", methods=["POST"])
def gemini_chat():
    data = request.get_json()
    user_msg = data.get("query", "").strip()

    if not user_msg:
        return jsonify({"answer": "Please enter a question."}), 400

    if not API_KEY:
        return jsonify({"answer": "API key not configured."}), 500

    url = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/gemini-1.5-flash-latest:generateContent"
    f"?key={API_KEY}"
)

payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": user_msg
                }
            ]
        }
    ]
}


    try:
        r = requests.post(url, json=payload, timeout=20)
        r.raise_for_status()
        res = r.json()

        text = res["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"answer": text})

    except Exception as e:
        return jsonify({"answer": f"AI error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

