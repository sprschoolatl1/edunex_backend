from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Load API key safely from Render Environment Variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/")
def home():
    return "Backend is running successfully!"

@app.route("/gemini", methods=["POST"])
def gemini():
    try:
        data = request.get_json()
        user_text = data.get("query", "")

        url = (
            "https://generativelanguage.googleapis.com/v1/models/"
            "gemini-2.0-flash:generateContent?key=" + GEMINI_API_KEY
        )

        body = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": f"""
You are an educational assistant. Follow these rules:

1. Keep answers short (2–3 lines).
2. Only give long answers when asked: 'explain in detail', 'elaborate', 'long answer'.

User question: {user_text}
"""
                        }
                    ]
                }
            ]
        }

        r = requests.post(url, json=body)
        result = r.json()
        print("RAW:", result)

        answer = (
            result.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "Gemini did not return text.")
        )

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"Backend error: {str(e)}"})


if __name__ == "__main__":
    app.run()
