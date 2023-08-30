import os
import glob

from explainer.lecture_app_engine import AppEngine


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
