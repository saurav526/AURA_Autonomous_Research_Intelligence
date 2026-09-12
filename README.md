# AURA — Autonomous Research & Intelligence

Full-stack Agentic AI research assistant using Groq + LangGraph + FastAPI + React.

## Features
- Planner agent
- Web research agent
- Analysis agent
- Adversarial verification agent
- Final synthesis agent
- Source collection/deduplication
- Confidence score
- React research dashboard



## Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and add:
```env
GROQ_API_KEY=your_groq_key
GROQ_MODEL=openai/gpt-oss-120b
```

Run:
```bash
uvicorn app.main:app --reload --port 8000
```

## Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173


## Download PDF
After a research run, click **Download PDF** under the final report. ReportLab generates `AURA_Research_Report.pdf`.

## Run anytime on Windows
After the first setup, double-click `START_AURA.bat`. It starts the FastAPI backend and React frontend in separate terminals and opens the application.

## Feedback
do forget to give star and suggestion for improvement 
