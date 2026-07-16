# Email Writing Assistant — Setup Guide (Beginner Friendly)

This project is a small backend service (built with **FastAPI**) that uses an
**LLM** (a large language model, like ChatGPT) to:
1. Generate emails from scratch
2. Suggest replies to an email you paste in
3. Fix grammar
4. Convert tone (e.g. casual → formal)
5. Translate emails to another language

It also comes with a simple test webpage so you don't need Postman to try it.

---

## 0. What you need installed on your computer

- **Python 3.10 or newer** — https://www.python.org/downloads/
  - While installing on Windows, tick **"Add Python to PATH"**.
- **VS Code** (or any code editor) — https://code.visualstudio.com/
- An **OpenAI API key** — https://platform.openai.com/api-keys
  - Sign up, add a small amount of credit ($5 is plenty for a project), then
    click "Create new secret key". Copy it somewhere safe — you won't be able
    to see it again.

Check Python is installed by opening a terminal (Command Prompt / Terminal /
VS Code's built-in terminal) and typing:
```
python --version
```
If that fails, try `python3 --version`.

---

## 1. Get the project files onto your computer

Put all these files in one folder called `email-assistant`:
```
email-assistant/
├── main.py
├── requirements.txt
├── .env.example
├── README.md
├── templates/
│   └── index.html
└── static/
    └── style.css
```
Open this folder in VS Code (`File → Open Folder`).

---

## 2. Create a virtual environment

A virtual environment keeps this project's packages separate from everything
else on your computer. In the terminal, **inside the `email-assistant`
folder**, run:

**Windows:**
```
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```
python3 -m venv venv
source venv/bin/activate
```

You'll know it worked because your terminal line now starts with `(venv)`.
You need to run the "activate" command every time you open a new terminal
for this project.

---

## 3. Install the required packages

With the virtual environment active:
```
pip install -r requirements.txt
```
This installs FastAPI, the OpenAI SDK, and a few small helper libraries.

---

## 4. Add your API key

1. Duplicate the file `.env.example` and rename the copy to `.env`
2. Open `.env` and replace the placeholder:
```
OPENAI_API_KEY=sk-your-real-key-here
```
3. Save the file. **Never share this file or upload it to GitHub** — it's
   your private key (add `.env` to a `.gitignore` file before pushing to
   GitHub, see step 8).

---

## 5. Run the project

Still inside the `email-assistant` folder with `(venv)` active, run:
```
uvicorn main:app --reload
```
You should see something like:
```
Uvicorn running on http://127.0.0.1:8000
```
Leave this terminal running — this is your server.

---

## 6. Try it out

Open your browser and go to:

- **http://127.0.0.1:8000/** → the test webpage. Try each tab (Generate,
  Reply, Grammar, Tone, Translate) and click the button — you'll see the
  AI's response appear below.

- **http://127.0.0.1:8000/docs** → FastAPI's automatic interactive API
  docs (Swagger UI). This is very useful to show in your internship demo —
  it lists all 5 endpoints, lets you fill in sample data, and shows you the
  exact request/response JSON. Click "Try it out" on any endpoint to test it.

---

## 7. How the project actually works (for your understanding / viva)

- `main.py` is the FastAPI app. Each feature is one "endpoint" — a URL that
  accepts a POST request with some JSON data.
- Every endpoint calls the helper function `ask_llm(system_prompt,
  user_prompt)`, which sends your text to OpenAI's model and returns its
  answer. The **system prompt** tells the model what role to play (e.g.
  "You are a grammar-correction assistant"); the **user prompt** contains the
  actual content to work on.
- `templates/index.html` + `static/style.css` make up the simple test
  webpage. It just calls your API endpoints using JavaScript's `fetch()`.
- Pydantic models (`GenerateEmailRequest`, `ReplyRequest`, etc.) define what
  fields are expected in each request, and FastAPI automatically validates
  incoming data against them.

### Endpoint summary

| Endpoint | Method | Purpose |
|---|---|---|
| `/generate-email` | POST | Write a new email from a purpose + key points |
| `/suggest-reply` | POST | Suggest a reply to a pasted email |
| `/check-grammar` | POST | Fix grammar/spelling |
| `/convert-tone` | POST | Rewrite text in a target tone |
| `/translate` | POST | Translate text to a target language |

---

## 8. Push it to GitHub (for your internship submission)

1. Create a `.gitignore` file in the folder with this content:
```
venv/
.env
__pycache__/
```
2. In the terminal:
```
git init
git add .
git commit -m "Email Writing Assistant - initial version"
```
3. Create a new empty repository on https://github.com (don't initialize
   with a README), then follow the commands GitHub shows you, e.g.:
```
git remote add origin https://github.com/your-username/email-assistant.git
git branch -M main
git push -u origin main
```

---

## 9. Common problems

- **"ModuleNotFoundError"** → your virtual environment isn't active, or you
  forgot `pip install -r requirements.txt`.
- **"Incorrect API key" / 401 error** → check your `.env` file has the right
  key and no extra spaces/quotes.
- **Nothing happens when you click a button on the webpage** → open your
  browser's Developer Tools (F12) → Console tab, to see the error.
- **Port already in use** → run `uvicorn main:app --reload --port 8001`
  instead, and use that port in the browser URL.

---

## 10. Ideas to extend this (good for your final report)

- Add a "summarize this email thread" endpoint.
- Add user accounts and save email history to a database (e.g. SQLite).
- Let the user pick between multiple LLM providers.
- Deploy it publicly using **Render** or **Railway** (both have free tiers)
  so you can share a live link in your internship report.
