import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq

# Load variables from the .env file (like your API key)
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"
app = FastAPI(title="Email Writing Assistant")

# Serve the simple test webpage
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def ask_llm(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content

# ---------------------------------------------------------------
# Request "shapes" (Pydantic models) — these define what JSON the
# frontend/Postman must send to each endpoint.
# ---------------------------------------------------------------

class GenerateEmailRequest(BaseModel):
    purpose: str
    key_points: str
    tone: str = "professional"
    recipient_name: str = ""

class ReplyRequest(BaseModel):
    original_email: str
    instructions: str = "Reply politely and address all points."
    tone: str = "professional"

class GrammarRequest(BaseModel):
    text: str

class ToneRequest(BaseModel):
    text: str
    target_tone: str

class TranslateRequest(BaseModel):
    text: str
    target_language: str


# ---------------------------------------------------------------
# Routes
# ---------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Serves the simple test webpage at http://localhost:8000/"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate-email")
def generate_email(req: GenerateEmailRequest):
    system_prompt = (
        "You are a professional email-writing assistant. "
        "Write clear, well-structured, ready-to-send emails."
    )
    user_prompt = f"""
    Write an email with the following details:
    Purpose: {req.purpose}
    Key points to include: {req.key_points}
    Tone: {req.tone}
    Recipient name: {req.recipient_name or "N/A"}

    Start with a subject line formatted exactly as "Subject: ...".
    """
    result = ask_llm(system_prompt, user_prompt)
    return {"email": result}


@app.post("/suggest-reply")
def suggest_reply(req: ReplyRequest):
    system_prompt = "You are an assistant that writes helpful, context-aware replies to emails."
    user_prompt = f"""
    Original email:
    {req.original_email}

    Instructions for the reply: {req.instructions}
    Tone: {req.tone}

    Write one complete, ready-to-send reply.
    """
    result = ask_llm(system_prompt, user_prompt)
    return {"reply": result}


@app.post("/check-grammar")
def check_grammar(req: GrammarRequest):
    system_prompt = (
        "You are a grammar-correction assistant. Fix grammar, spelling, and "
        "punctuation mistakes without changing the meaning or tone. "
        "Return ONLY the corrected text, nothing else."
    )
    result = ask_llm(system_prompt, req.text)
    return {"corrected_text": result}


@app.post("/convert-tone")
def convert_tone(req: ToneRequest):
    system_prompt = (
        f"You rewrite text to match this tone: {req.target_tone}. "
        "Keep the original meaning and roughly the same length. "
        "Return ONLY the rewritten text."
    )
    result = ask_llm(system_prompt, req.text)
    return {"converted_text": result}


@app.post("/translate")
def translate(req: TranslateRequest):
    system_prompt = (
        f"You are a professional translator. Translate the given text into "
        f"{req.target_language}, preserving tone and meaning. "
        "Return ONLY the translation."
    )
    result = ask_llm(system_prompt, req.text)
    return {"translated_text": result}
