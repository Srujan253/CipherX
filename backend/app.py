from flask import Flask, request, jsonify
from flask_cors import CORS
from textblob import TextBlob
from langdetect import detect

app = Flask(__name__)
CORS(app)  # allow React frontend to connect

@app.route('/api/check', methods=['POST'])
def check_english():
    data = request.get_json()
    text = data.get("text", "").strip().lower()

    try:
        lang = detect(text)
        blob = TextBlob(text)
        score = blob.sentiment.polarity

        is_english = lang == "en"
        result = {
            "input": text,
            "is_english": is_english,
            "sentiment_score": score
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
