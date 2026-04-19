from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    files = relationship("File", back_populates="owner")


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)               # original filename shown to user
    type = Column(String, nullable=False)               # MIME type
    size = Column(Integer, nullable=False)              # size in bytes
    date = Column(DateTime, default=datetime.utcnow)
    stored_name = Column(String, nullable=False)        # UUID-based name on disk
    hashed_file_password = Column(String, nullable=False)

    owner = relationship("User", back_populates="files")
