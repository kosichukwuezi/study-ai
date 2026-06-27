from flask import Flask, render_template, request
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    notes = request.form["notes"]

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": f"Summarize these lecture notes clearly and concisely:\n\n{notes}"}
        ]
    )

    summary = message.content[0].text
    
    return render_template("result.html",notes = summary )

if __name__ == "__main__":
    app.run(debug=True, port=5002)
