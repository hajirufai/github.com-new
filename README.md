# STEMflow ⚡ — Socratic AI STEM Tutor

> *Built for [DSH Hacks V1](https://dsh-hacks-v1.devpost.com/) — STEM AI for Students*

**STEMflow** is an AI-powered STEM tutor that teaches students by asking guiding questions — not by handing out answers. Like the best human tutors, it uses the **Socratic method** to help students aged 13+ discover answers themselves, building real understanding instead of memorization.

---

## The Problem

Students struggle with STEM because most AI tools give them the answer directly. Copy-pasting a solution doesn't build understanding. When the exam comes, the learning hasn't happened.

## The Solution

STEMflow flips the script. Ask it "What is the quadratic formula?" and instead of just telling you, it asks: *"What do you already know about solving for x? Let's start there."* It guides you step by step until you discover the answer yourself — and actually understand it.

**Key features:**
- 🧠 **Socratic dialogue** — guides thinking, never just gives answers
- 📚 **5 STEM subjects** — Math, Physics, Chemistry, Biology, Computer Science
- 🎯 **Adaptive levels** — Auto/Beginner/Intermediate/Advanced
- 💡 **Smart hints** — gives nudges before full explanations
- ⚡ **Real-time chat** — fast, mobile-friendly interface

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12 + FastAPI |
| AI | Google Gemini 1.5 Flash API |
| Frontend | Vanilla HTML/CSS/JS (zero dependencies) |
| Deploy | Docker + Google Cloud Run / Vercel |

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/hajirufai/stemflow
cd stemflow

# Install dependencies
pip install -r requirements.txt

# Set your Gemini API key (free at https://aistudio.google.com/app/apikey)
export GOOGLE_API_KEY=your_key_here

# Run
python app/main.py
# → Opens at http://localhost:8080
```

---

## Deploy to Google Cloud Run

```bash
# Build and push Docker image
gcloud builds submit --tag gcr.io/YOUR_PROJECT/stemflow

# Deploy
gcloud run deploy stemflow \
  --image gcr.io/YOUR_PROJECT/stemflow \
  --set-env-vars GOOGLE_API_KEY=your_key_here \
  --platform managed \
  --allow-unauthenticated \
  --port 8080
```

---

## Judging Criteria Alignment

| Criteria | STEMflow's approach |
|---------|-------------------|
| **Idea (30pts)** | Socratic method is pedagogically proven — different from every Q&A chatbot |
| **Implementation (30pts)** | Full working app with FastAPI backend, Gemini AI, real-time chat |
| **Design (20pts)** | Dark-mode UI built for students, mobile-responsive, clean UX |
| **Presentation (20pts)** | Clear problem: rote memorization vs. real understanding |

---

## How It Works

1. Student asks a STEM question
2. STEMflow checks what the student already knows (probing question)
3. Breaks the concept into steps, asks one at a time
4. If stuck: gives a **hint** not the answer
5. Student arrives at the answer themselves
6. STEMflow asks student to explain it back in their own words

This mirrors proven pedagogical research showing students retain 90% more from active discovery vs. passive reception.

---

## Project Structure

```
stemflow/
├── app/
│   ├── main.py          # FastAPI backend + Gemini integration
│   ├── templates/
│   │   └── index.html   # Frontend UI (single file, no framework needed)
│   └── static/          # Static assets (future: icons, etc.)
├── requirements.txt
├── Dockerfile
└── README.md
```

---

*Built with ❤️ for DSH Hacks V1 — making STEM education accessible, engaging, and effective.*
