# Task Tracker API (Module 1)

A minimal learning-project REST API built with Python, FastAPI, and Pydantic. This module includes only a health check endpoint; task CRUD functionality is not yet implemented.

## Setup

Create and activate a virtual environment, then install dependencies:

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Running the server

```bash
uvicorn app.main:app --reload --port 8000
```

## Testing the health endpoint

```bash
curl http://localhost:8000/health

Better option: 
Invoke-RestMethod http://127.0.0.1:8000/health
```

Expected response:
```json
{
  "status": "ok",
  "timestamp": "2026-08-05T12:00:00+00:00"
}
```

## API docs

Once running, open `http://localhost:8000/docs` for the Swagger UI.

## Frontend
cd frontend
python -m http.server 5500 