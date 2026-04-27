from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
import shutil

from database import get_db
import models
import schemas
from auth import get_current_user, hash_password, verify_password
from utils.file_utils import generate_stored_name, get_file_path, get_upload_dir

router = APIRouter(prefix="/api/files", tags=["Files"])


@router.get("", response_model=List[schemas.FileOut])
def get_all_files(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Return all files belonging to the current user."""
    files = db.query(models.File).filter(models.File.user_id == current_user.id).all()
    return files


@router.post("/upload", response_model=schemas.FileOut, status_code=201)
async def upload_file(
    file: UploadFile = File(...),
    password: str = Form(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a file with a protection password."""
    stored_name = generate_stored_name(file.filename)
    file_path = get_file_path(stored_name)

    # Save file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(file_path)
    mime_type = file.content_type or "application/octet-stream"

    db_file = models.File(
        user_id=current_user.id,
        name=file.filename,
        type=mime_type,
        size=file_size,
        stored_name=stored_name,
        hashed_file_password=hash_password(password)
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return db_file


@router.get("/{file_id}", response_model=schemas.FileOut)
def get_file(
    file_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Return metadata for a single file."""
    db_file = db.query(models.File).filter(
        models.File.id == file_id,
        models.File.user_id == current_user.id
    ).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found.")
    return db_file


@router.post("/{file_id}/unlock", response_model=schemas.UnlockResponse)
def unlock_file(
    file_id: int,
    payload: schemas.UnlockRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Verify the file password. Returns true/false — does NOT return file content."""
    db_file = db.query(models.File).filter(
        models.File.id == file_id,
        models.File.user_id == current_user.id
    ).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found.")

    is_correct = verify_password(payload.password, db_file.hashed_file_password)
    return {"success": is_correct}


@router.get("/{file_id}/download")
def download_file(
    file_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download the actual file. Frontend should call /unlock first to verify the password."""
    db_file = db.query(models.File).filter(
        models.File.id == file_id,
        models.File.user_id == current_user.id
    ).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found.")

    file_path = get_file_path(db_file.stored_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on disk.")

    return FileResponse(
        path=file_path,
        filename=db_file.name,
        media_type=db_file.type,
        headers={"Content-Disposition": f'attachment; filename="{db_file.name}"'}
    )


@router.delete("/{file_id}", response_model=schemas.MessageResponse)
def delete_file(
    file_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a file from disk and from the database."""
    db_file = db.query(models.File).filter(
        models.File.id == file_id,
        models.File.user_id == current_user.id
    ).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found.")

    # Delete from disk if it exists
    file_path = get_file_path(db_file.stored_name)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(db_file)
    db.commit()

    return {"message": "File deleted successfully."}
