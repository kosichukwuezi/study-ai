
from io import Reader

import markdown
from flask import Flask, render_template, request
import anthropic #import the anthropic library
import os # import the os library to access environment variables
from dotenv import load_dotenv # import the env where the API key is stored
import json 
from pypdf import PdfReader

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

    uploaded = request.files.get("pdf") #get the uploaded file if any
    if uploaded and uploaded.filename != "": #check if a file was uploaded
        reader = PdfReader(uploaded)
        pdf_text =""
        for page in reader.pages:
            pdf_text +=page.extract_text()
        notes = pdf_text #replace the notes with the text extracted from the PDF


    # choose the instruction based on the mode
    if mode == "quiz":
        prompt = f"""Create 5 quiz questions based on these notes. Return ONLY a JSON array, no other text or markdown.
Format: [{{"question": "...", "answer": "..."}}]
Notes:
{notes}"""
    elif mode == "practice":
        prompt = f"""Create 20 flashcards based on these notes.The "front" must be a QUESTION or TERM only (never the answer).
    The "back" must be the answer or definition.
    Return ONLY a JSON array, no other text or markdown.
    Format: [{{"front": "What is a stack?", "back": "A LIFO data structure where you add and remove from the top"}}]
    Notes:
    {notes}"""
        
    elif mode == "flashcards":
            prompt = f"""Create 10 flashcards based on these notes.
    The "front" must be a QUESTION or TERM only (never the answer).
    The "back" must be the answer or definition.
    Return ONLY a JSON array, no other text or markdown.
    Format: [{{"front": "What is a stack?", "back": "A LIFO data structure where you add and remove from the top"}}]

    Notes:
    {notes}"""
            
    else:
        prompt = f"""You are a study assistant. Create study-focused notes from the material below.

    Structure your response as:
    1. **Key Concepts** — the main ideas, each explained in 1-2 clear sentences
    2. **Important Terms** — bold each key term with its definition
    3. **What to Focus On** — flag the 3-4 most exam-relevant points
    4. **Quick Review** — 3-5 bullet takeaways for fast revision

    Keep explanations clear and tied to the source material. Preserve any formulas, definitions, or specific facts exactly. If the material references a diagram or figure, mention it by name so the student knows to review it.

    Material:
    {notes}"""


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
        start = raw.find("[") # find the start of the JSON array in the response
        end = raw.rfind("]") + 1 # find the end of the JSON array in the response
        json_part = raw[start:end] # extract the JSON array from the response
        questions = json.loads(json_part) # convert the JSON array to a Python list of dictionaries
        return render_template("quiz.html", questions=questions) # render the quiz.html template with the questions
    
    elif mode == "flashcards":
        start = raw.find("[")
        end = raw.rfind("]") + 1
        cards = json.loads(raw[start:end])
        return render_template("flashcards.html", cards=cards)
    
    elif mode == "practice":
        start = raw.find("[")
        end = raw.rfind("]") + 1
        cards = json.loads(raw[start:end])
        return render_template("practice.html", cards=cards)    
     
    else:
        result =markdown.markdown(raw, extensions=["tables"]) # convert the summary to HTML format using the markdown library
        return render_template("result.html", notes=result)
if __name__ == "__main__":
    app.run(debug=True, port=5002)
