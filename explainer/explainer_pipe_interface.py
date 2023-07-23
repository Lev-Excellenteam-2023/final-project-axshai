import os
import glob
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session
import db_interface.tables as db
from db_interface.tables import Upload
from explainer.lecture_app_engine import AppEngine
from web_api.web_app import RequestStatus


class Pipe:
    """Interface representing a pipe."""

    def _create(self):
        """Create method for the pipe. Raises NotImplementedError."""
        raise NotImplementedError

    def receive(self):
        """Receive method for the pipe. Raises NotImplementedError."""
        raise NotImplementedError

    def send(self, lecture):
        """Send method for the pipe. Raises NotImplementedError."""
        raise NotImplementedError

    def pop(self):
        """Pop method for the pipe. Raises NotImplementedError."""
        raise NotImplementedError


class FileSystemPipe(Pipe):
    """Class representing a file system pipe."""

    def __init__(self, lectures_folder, destination_folder):
        """
        Initialize the FileSystemPipe.

        Args:
            lectures_folder (str): Path to the folder containing lectures.
            destination_folder (str): Path to the destination folder.

        """
        self.__front = None
        self._lectures_folder = lectures_folder
        self._destination_folder = destination_folder
        self._create()

    def _create(self):
        """Create method for the file system pipe."""
        if not os.path.exists(self._lectures_folder):
            # Create the directory
            os.makedirs(self._lectures_folder)
        if not os.path.exists(self._destination_folder):
            # Create the directory
            os.makedirs(self._destination_folder)

    def send(self, lecture):
        """
        Send the lecture through the file system pipe.

        Args:
            lecture: The lecture to send.

        """
        explainer_engine = AppEngine(lecture, self._destination_folder)
        explainer_engine.run_app()

    def receive(self):
        """
        Receive the oldest file from the file system pipe.

        Returns:
            str: The path to the oldest file.

        """
        oldest_file = None
        file_list = glob.glob(os.path.join(self._lectures_folder, '*'))
        if file_list:
            oldest_file = min(file_list, key=os.path.getctime)
        self.__front = oldest_file
        return self.__front

    def pop(self):
        """
        Remove the oldest file from the file system pipe.

        If the file exists, it is removed and the next oldest file becomes the new front.

        """
        if self.__front and os.path.exists(self.__front):
            os.remove(self.__front)
            self.receive()


class DataBasePipe(Pipe):
    """Class representing a DataBase pipe."""

    def __init__(self, lectures_folder, destination_folder):
        """
        Initialize the DataBasePipe.

        Args:
            lectures_folder (str): Path to the folder containing lectures.
            destination_folder (str): Path to the destination folder.

        """
        self.__front = None
        self.__upload = None
        self.__engine = db.get_engine()
        self._lectures_folder = lectures_folder
        self._destination_folder = destination_folder
        self._create()

    def _create(self):
        """Create method for the Data Base pipe."""
        if not os.path.exists(self._destination_folder):
            # Create the directory
            os.makedirs(self._destination_folder)

    def send(self, lecture):
        """
        Send the lecture through the Data Base pipe.

        Args:
            lecture: The lecture to send.

        """
        with Session(self.__engine) as session:
            if self.__upload:
                self.__upload.status = RequestStatus.PROCESSING
                session.add(self.__upload)
                session.commit()
        explainer_engine = AppEngine(lecture, self._destination_folder)
        explainer_engine.run_app()
        self.__upload.finish_time = datetime.now()
        with Session(self.__engine) as session:
            self.__upload.status = RequestStatus.DONE
            session.add(self.__upload)
            session.commit()

    def receive(self):
        """
        Receive the oldest file from the  Data Base pipe.

        Returns:
            str: The path to the oldest file.

        """
        with Session(self.__engine) as session:
            select_statement = select(Upload).where(Upload.status == RequestStatus.PENDING)\
                .order_by(Upload.upload_time)
            ordered_uploads_list = session.scalars(select_statement).all()
            if ordered_uploads_list:
                self.__upload = ordered_uploads_list[0]
                self.__front = self.__upload.upload_path(self._lectures_folder)
            else:
                self.__upload = self.__front = None
        return self.__front

    def pop(self):
        """
        pop the oldest file from the DB pipe.
        If the file exists, it is pop and the next oldest file becomes the new front.

        """
        if self.__front:
            self.receive()
