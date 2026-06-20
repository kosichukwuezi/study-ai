# STUDY AI

A free web app that turns lecture notes into study material ,summaries, quizzes, and flashcards, using AI. Built to  genuinely free, with no paywalls or usage limits.

## Why I built this
I more specifically built this with my experience using online AI study apps in mind, while a common concept, a lot of study tools hide behind giant paywalls, or usage limits. I wanted a fast and visual way to turn messy or lengthy lecture notes into something useful for exam prep.

## What it does
- Paste in lecture notes or any text
- Choose a mode: summarize, generate quiz questions, or make flashcards
- Get back AI-generated study material instantly

*(PDF, screenshot, and voice input are planned — see roadmap below.)*

## Tech stack
- **Backend:** Python + Flask
- **AI:** (OpenAI / Anthropic API)
- **Frontend:** HTML, CSS
- **Version control:** Git + GitHub

## Status
🚧 In progress — building the core request/response flow first, then connecting the AI.

## Planned features

### V1 (core — building now)
- [x] Flask app with a notes input form
- [ ] Echo route — proving the request cycle
- [ ] Connect AI API for real summaries
- [ ] Paste-in text → summary mode
- [ ] Quiz-generation mode
- [ ] Flashcard mode
- [ ] Styling with CSS
- [ ] Deploy live with a public link

### Future roadmap
- [ ] "Teach the lecture" mode
- [ ] Exam-style questions (university standard)
- [ ] PDF upload support
- [ ] Screenshot / image input (OCR)
- [ ] Voice recording input (audio transcription)

## How to run locally
1. Clone the repo
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install flask`
5. Run: `python3 app.py`
6. Open http://127.0.0.1:5002
