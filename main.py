from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from database import engine, Base
from routers import auth, files
from utils.file_utils import get_upload_dir

load_dotenv()

# Create DB tables on startup
Base.metadata.create_all(bind=engine)

# Ensure uploads directory exists
get_upload_dir()

app = FastAPI(
    title="VaultSafe API",
    description="Backend for VaultSafe — Digital Asset Protection",
    version="1.0.0"
)

# CORS — allow frontend origins (set ALLOWED_ORIGINS env var as comma-separated list, or "*" for all)
raw_origins = os.getenv("ALLOWED_ORIGINS", "*")
if raw_origins == "*":
    allow_origins = ["*"]
else:
    allow_origins = [o.strip() for o in raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=raw_origins != "*",  # credentials not allowed with wildcard
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(files.router)


@app.get("/")
def root():
    return {"message": "VaultSafe API is running. Visit /docs for the Swagger UI."}
