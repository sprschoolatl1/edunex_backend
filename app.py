from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = "AIzaSyDIJyYtqwajZAcxywUQWZGrIFEK3PLFsW4"

@app.route("/")
def home():
    return "Backend is working!"

@app.route("/gemini", methods=["POST"])
def gemini():
    data = request.get_json()
    user_text = data.get("query", "")

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    body = {
        "contents": [
            {
                "role": "user",
                "parts": [ {"text": user_text} ]
            }
        ]
    }

    response = requests.post(url, json=body)
    result = response.json()

    print("RAW GEMINI RESPONSE:", result)

    # ---- SAFE TEXT EXTRACTION ----
   try:
    answer = result["candidates"][0]["content"]["parts"][0]["text"]
except:
    answer = "Gemini did not return a valid message."

    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run()

