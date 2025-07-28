# Messmate-Web
A web-based digital mess subscription platform for students and mess owners. Discover messes, subscribe to meal plans, scan QR codes for meal access, and manage operations with an admin dashboard.

# Messmate Backend Setup

## Clone the Project

```bash
git clone https://github.com/BroCodeByMinds/messmate-web.git
```

## ⚙️ Run the Setup Batch File

Path to script:
```
C:\Users\Gopal\Documents\messmate-web\backend\setup_backend.bat
```

### This script will:
- Create a virtual environment if it does not exist
- Activate the environment
- Install all required dependencies from `requirements.txt`

## ▶️ Run the FastAPI Server

Make sure you're in the backend directory, then run:

```bash
uvicorn app.main:app --reload
```

This will start the server at: [http://127.0.0.1:8000](http://127.0.0.1:8000)