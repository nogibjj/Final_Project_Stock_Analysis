from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Load sentiment analysis model from Hugging Face
sentiment_analysis = pipeline("sentiment-analysis")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if request.method == "POST":
        text = request.form["text"]
        # Perform sentiment analysis on the provided text
        result = sentiment_analysis(text)
        sentiment = result[0]["label"]
        return render_template("result.html", text=text, sentiment=sentiment)


if __name__ == "__main__":
    app.run(debug=True)
