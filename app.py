from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = "AIzaSyDIJyYtqwajZAcxywUQWZGrIFEK3PLFsW4"

@app.route("/gemini", methods=["POST"])
def gemini():
    data = request.get_json()
    user_text = data.get("query", "")

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    body = {
    "contents": [
        {
            "role": "user",
            "parts": [{
                "text": f"""
You are an educational assistant. Follow these rules STRICTLY:

1. ALWAYS give a short answer of 2–3 lines ONLY.
2. ONLY give long/detail answers if the user says:
   - "explain in detail"
   - "give long answer"
   - "full explanation"
   - "elaborate"
   - "describe fully"
   - "long explanation"

User question: {user_text}
"""
            }]
        }
    ]
}

    response = requests.post(url, json=body)
    result = response.json()

    print("\nRAW GEMINI RESPONSE:", result)  # <-- debugging

    answer = (
        result.get("candidates", [{}])[0]
             .get("content", {})
             .get("parts", [{}])[0]
             .get("text", "Gemini did not return text.")
    )

    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True)
