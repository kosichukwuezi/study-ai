from curses import raw

import markdown
from flask import Flask, render_template, request
import anthropic #import the anthropic library
import os # import the os library to access environment variables
from dotenv import load_dotenv # import the env where the API key is stored
import json 

load_dotenv()

app = Flask(__name__)
app.jinja_env.globals.update(enumerate=enumerate) #makes enumerate work in templates
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY")) # initialize the anthropic client with the API key

@app.route("/") #home page action
def home():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"]) #summarize action
def summarize():
    notes = request.form["notes"] #get the notes from the submission
    mode = request.form["mode"] #get which mode the user selected

    # choose the instruction based on the mode
    if mode == "quiz":
        prompt = f"""Create 5 quiz questions based on these notes. Return ONLY a JSON array, no other text or markdown.
Format: [{{"question": "...", "answer": "..."}}]

Notes:
{notes}"""
        
    else:
        prompt = f"Summarize these lecture notes clearly and concisely:\n\n{notes}"


    message = client.messages.create(
        model="claude-haiku-4-5-20251001", #what claude model to use
        max_tokens=1000, #message length limit
        messages=[
            {"role": "user", "content": prompt}
        ] #the message sent to the model for summarization 
    ) 

    raw = message.content[0].text.strip()

    #Handle the response differently based on the mode
    if mode == "quiz":
        start = raw.find("[")
        end = raw.rfind("]") + 1
        json_part = raw[start:end]
        questions = json.loads(json_part)
        return render_template("quiz.html", questions=questions)
    else:
        result =markdown.markdown(raw, extensions=["tables"]) # convert the summary to HTML format using the markdown library
        return render_template("result.html", notes=result)
if __name__ == "__main__":
    app.run(debug=True, port=5002)
