# CrewAI Multi-Agent Platform

A modern, extensible AI assistant platform built with FastAPI (Python backend) and a beautiful, interactive frontend. The system features a multi-agent dashboard, with a fully functional Academic Research Assistant powered by Groq LLM, and placeholders for future agents (YouTube, Code, Business, Data Analysis).

---

## Features

- **Multi-Agent Dashboard**: Modern homepage to launch specialized AI agents.
- **Academic Research Assistant**: Ask academic questions across disciplines and get comprehensive, AI-generated answers.
- **FastAPI Backend**: Robust REST API with async support, CORS, error handling, and health checks.
- **Groq LLM Integration**: Uses Groq API for high-quality, fast AI responses.
- **Frontend**: Responsive, animated dashboard and chat UI (HTML/CSS/JS).
- **Extensible**: Easily add new agents and services.

---

## Project Structure

```
Crew-AI-Agent/
│
├── backend/
│   ├── main.py                # FastAPI app entry point
│   ├── src/
│   │   ├── routes/
│   │   │   ├── academic.py    # Academic agent API routes
│   │   │   └── health.py      # Health check endpoint
│   │   ├── services/
│   │   │   └── academic_service.py # Academic agent logic (Groq API)
│   │   └── config.py          # Configuration (env, API keys)
│   └── ...
│
├── frontend/
│   ├── home.html              # Multi-agent dashboard homepage
│   ├── academic.html          # Academic chat agent UI
│   ├── script.js              # Academic chat frontend logic
│   ├── home.js                # Dashboard interactivity
│   ├── home.css               # Dashboard styles
│   └── styles.css             # Academic chat styles
│
├── requirements.txt           # Python dependencies
└── README.md                  # (You are here)
```

---

## Backend Overview

- **main.py**: Sets up FastAPI app, CORS, error handling, static file serving, and includes routers.
- **/src/routes/academic.py**: 
  - `/api/v1/academic/chat` (POST): Accepts `{question, subject}` and returns `{message, subject}`.
  - `/api/v1/academic/subjects` (GET): Returns available subjects.
- **/src/services/academic_service.py**: Handles prompt construction and calls Groq API for completions.
- **/src/config.py**: Loads environment variables (API keys, model, etc).

### Environment Variables

Set these in a `.env` file in `backend/`:

```
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
```

---

## Frontend Overview

- **home.html**: Dashboard with agent cards (Academic agent is live, others are "Coming Soon").
- **academic.html**: Chat interface for the academic agent.
- **script.js**: Handles chat UI, sends POST requests to `/api/v1/academic/chat`, displays responses.
- **home.js**: Handles dashboard interactivity, agent status, and navigation.
- **home.css**: Modern, responsive dashboard styles.

---

## Running the Project

1. **Install Python dependencies** (in `backend/`):
   ```bash
   python3 -m vev venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Set environment variables** in `backend/.env` (see above).

3. **Start the backend server**:
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload --port 8000
   ```

4. **Open the dashboard**:
   - Go to [http://localhost:8000/](http://localhost:8000/) in your browser.

---

## API Endpoints

- `GET /api/v1/health` — Health check
- `POST /api/v1/academic/chat` — Academic Q&A (`{"question": "...", "subject": "..."}`)
- `GET /api/v1/academic/subjects` — List of subjects

---

## Extending the Platform

- Add new agents by creating new route, service, and frontend files.
- Update `home.html` and `home.js` to add new agent cards and navigation.
- Follow the Academic agent pattern for new AI assistants.

---

## License

MIT

---

## Credits

- FastAPI, Groq, Font Awesome, Inter font, and all open-source dependencies.

---

Feel free to further customize this README for your team or deployment!
