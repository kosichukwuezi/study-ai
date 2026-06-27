import markdown
from flask import Flask, render_template, request
import anthropic #import the anthropic library
import os # import the os library to access environment variables
from dotenv import load_dotenv # import the env where the API key is stored

load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY")) # initialize the anthropic client with the API key

@app.route("/") #home page action
def home():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"]) #summarize action
def summarize():
    notes = request.form["notes"] #get the notes from the submission

    message = client.messages.create(
        model="claude-haiku-4-5-20251001", #what claude model to use
        max_tokens=1000, #message length limit
        messages=[
            {"role": "user", "content": f"Summarize these lecture notes clearly and concisely:\n\n{notes}"}
        ] #the message sent to the model for summarization 
    ) 

    summary = markdown.markdown(message.content[0].text, extensions=["tables"]) # convert the summary to HTML format using the markdown library
    
    return render_template("result.html", notes=summary) # return the summary to the result.html template

if __name__ == "__main__":
    app.run(debug=True, port=5002)
