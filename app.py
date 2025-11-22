from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Use environment variable instead of hardcoding
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/gemini", methods=["POST"])
def gemini():
    try:
        data = request.get_json()
        user_text = data.get("query", "")

        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

        body = {
            "contents": [{
                "role": "user",
                "parts": [{
                    "text": f"""
Answer in short (2–3 lines).
Long answer only if user says 'explain in detail'.

User question: {user_text}
"""
                }]
            }]
        }

        response = requests.post(url, json=body)
        result = response.json()

        print("RAW RESULT:", result)

        # Extract safe message
        if "candidates" in result:
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"answer": text})

        return jsonify({"answer": "Gemini did not return a valid message."})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"answer": f"Backend error: {str(e)}"})

@app.route("/", methods=["GET"])
def home():
    return "Backend is running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
