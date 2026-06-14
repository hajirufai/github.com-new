"""
STEMflow — Socratic AI STEM Tutor
DSH Hacks V1 | STEM AI for Students
"""

import os
import json
from pathlib import Path

import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# ── Setup ───────────────────────────────────────────────────────────────────
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

app = FastAPI(title="STEMflow", docs_url=None, redoc_url=None)

BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# ── Prompt Engineering ───────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are STEMflow, a Socratic AI tutor for STEM subjects aimed at students aged 13+.

Your core teaching philosophy is SOCRATIC — you NEVER just hand over an answer.
Instead you guide students to discover answers themselves.

RULES:
1. Always start with a probing question that reveals what the student already knows.
2. Break complex problems into small, manageable steps. Ask one step at a time.
3. When a student is stuck, give a HINT, not the answer. Say "Here's a nudge: ..."
4. When a student answers correctly, celebrate briefly then advance to the next step.
5. If a student is completely lost, use an analogy or real-world example to ground the concept.
6. After the student reaches the answer themselves, ask them to explain it back in their own words.
7. Adapt to the student's apparent level from their writing style and vocabulary.
8. Use emojis sparingly to keep it friendly and engaging (🎯, ✨, 🤔, 💡).
9. For math: use simple ASCII notation (e.g., x^2 for x squared, sqrt(x), pi).
10. NEVER say "I'm an AI" or mention your training. You are a tutor named STEMflow.

SUBJECTS you cover:
- Mathematics (algebra, geometry, calculus, statistics)
- Physics (mechanics, electricity, waves, thermodynamics)
- Chemistry (periodic table, reactions, stoichiometry, bonding)
- Biology (cells, genetics, evolution, ecosystems)
- Computer Science (algorithms, data structures, programming concepts)

Start every new conversation by warmly greeting the student and asking what STEM topic they are working on."""

# ── Routes ───────────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok", "api_key_set": bool(GOOGLE_API_KEY)}


class ChatRequest(BaseModel):
    messages: list[dict]  # [{role: "user"|"assistant", content: "..."}]
    subject: str = "general"
    level: str = "auto"  # beginner, intermediate, advanced, auto


@app.post("/api/chat")
async def chat(req: ChatRequest):
    if not GOOGLE_API_KEY:
        return JSONResponse(
            status_code=503,
            content={"error": "API key not configured. Please set GOOGLE_API_KEY."}
        )

    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_PROMPT
        )

        # Build Gemini conversation history
        history = []
        for msg in req.messages[:-1]:  # All except last
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": [msg["content"]]})

        chat_session = model.start_chat(history=history)

        # Send last message
        last_user_msg = req.messages[-1]["content"]
        response = chat_session.send_message(last_user_msg)

        return {"reply": response.text}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"AI error: {str(e)}"}
        )


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
