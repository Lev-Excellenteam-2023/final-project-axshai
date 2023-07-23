import os
import uuid
from datetime import datetime
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db_interface import engine


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass


class User(Base):
    """Represents a User entity in the database.

     :param id: The primary key of the user (auto incremented).
     :param email: The email address of the user (unique and non-nullable).
     :param uploads: A list of Upload objects associated with this user.
     """
    __tablename__ = "User"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    uploads: Mapped[List["Upload"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r}"


class Upload(Base):
    """Represents an Upload entity in the database.

       :param id: The primary key of the upload (auto incremented).
       :param uid: The UUID of the upload (generated automatically and unique).
       :param filename: The name of the uploaded file (non-nullable).
       :param upload_time: The time when the file was uploaded (non-nullable).
       :param finish_time: The time when the explanation process is finished (nullable).
       :param status: The status of the upload.
       :param user_id: The foreign key referencing the User entity (nullable).
       :param user: The User object associated with this upload.
       :return: None
       """
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
        """Computes the path of the uploaded file based on metadata in the DB.

        :param base_path: The base directory where the file will be stored. Default is the current directory.
        :return: The computed path for the uploaded file.
        """
        return os.path.join(base_path, f"{self.uid}.{self.filename.split('.')[-1]}")

    def output_path(self, base_path="."):
        """Computes the path of the explained uploaded file based on metadata in the DB.

        :param base_path: The base directory where the file will be stored. Default is the current directory.
        :return: The computed path for the explained uploaded file.
        """
        return os.path.join(base_path, f"{self.uid}.{'json'}")


# Base.metadata.create_all(engine)

def get_engine():
    """Get the SQLAlchemy engine.

    :return: The SQLAlchemy engine.
    """
    return engine
