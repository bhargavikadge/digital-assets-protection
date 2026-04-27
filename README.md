# VaultSafe — Backend API

FastAPI backend for VaultSafe, a Digital Asset Protection app.

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
# Edit .env and set a strong SECRET_KEY before running in production

# 4. Start the server
uvicorn main:app --reload
```

The API runs at: `http://localhost:8000`  
Swagger docs: `http://localhost:8000/docs`

## Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /api/auth/register | No | Register a new user |
| POST | /api/auth/login | No | Login, returns JWT |
| GET | /api/files | Yes | List all your files |
| POST | /api/files/upload | Yes | Upload a protected file |
| GET | /api/files/{id} | Yes | Get file metadata |
| POST | /api/files/{id}/unlock | Yes | Verify file password |
| GET | /api/files/{id}/download | Yes | Download file |
| DELETE | /api/files/{id} | Yes | Delete file |

## Auth

All protected routes require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <your_token>
```

Get your token from `/api/auth/login` or `/api/auth/register`.
