import os
import uuid


def get_upload_dir() -> str:
    upload_dir = os.getenv("UPLOAD_DIR", "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir


def generate_stored_name(original_filename: str) -> str:
    """Generate a UUID-based filename preserving the original extension."""
    ext = os.path.splitext(original_filename)[-1]
    return f"{uuid.uuid4()}{ext}"


def get_file_path(stored_name: str) -> str:
    return os.path.join(get_upload_dir(), stored_name)
