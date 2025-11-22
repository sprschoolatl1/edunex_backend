from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = "AIzaSyDIJyYtqwajZAcxywUQWZGrIFEK3PLFsW4"

@app.route("/gemini", methods=["POST"])
def gemini_chat():
    data = request.get_json()
    user_msg = data.get("query", "")

    if not user_msg:
        return jsonify({"answer": "No query received"}), 400

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-1.5-flash:generateContent?key=" + API_KEY
    )

    payload = {
        "contents": [{"role": "user", "parts": [{"text": user_msg}]}]
    }

    try:
        r = requests.post(url, json=payload)
        response = r.json()

        print("Gemini raw:", response)

        # extract text safely
        answer = (
            response.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )

        if not answer:
            return jsonify({"answer": "Gemini did not return text"}), 200

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"}), 500


@app.route("/", methods=["GET"])
def home():
    return "Backend running successfully"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
