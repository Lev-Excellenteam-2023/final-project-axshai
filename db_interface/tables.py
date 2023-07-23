import os
import uuid
from datetime import datetime
from typing import List
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from db_interface import engine


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "User"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    uploads: Mapped[List["Upload"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r}"


class Upload(Base):
    __tablename__ = "Upload"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uid: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, unique=True, nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    upload_time: Mapped[datetime] = mapped_column(nullable=False)
    finish_time: Mapped[datetime] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"), nullable=True)
    user: Mapped["User"] = relationship(back_populates="uploads")

    def __repr__(self) -> str:
        return f"Upload(id={self.id!r}, uid={self.uid!r}), filename={self.filename!r}), " \
               f"upload_time={self.upload_time!r}), status={self.status!r}), user_id={self.user_id!r})"

    def upload_path(self, base_path="."):
        """Computes the path of the uploaded file based on metadata in the DB."""
        return os.path.join(base_path, f"{self.uid}.{self.filename.split('.')[-1]}")

    def output_path(self, base_path="."):
        """Computes the path of the explained uploaded file based on metadata in the DB."""
        return os.path.join(base_path, f"{self.uid}.{'json'}")


# Base.metadata.create_all(engine)

def get_engine():
    return engine
