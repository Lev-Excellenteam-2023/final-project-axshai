import os
import glob

from explainer.lecture_app_engine import AppEngine


class Pipe:
    def receive(self):
        raise NotImplementedError

    def send(self, lecture):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError


class FileSystemPipe(Pipe):
    def __init__(self, lectures_folder, destination_folder):
        self.__front = None
        self._lectures_folder = lectures_folder
        self._destination_folder = destination_folder

    def send(self, lecture):
        explainer_engine = AppEngine(lecture, self._destination_folder)
        explainer_engine.run_app()

    def receive(self):
        oldest_file = None
        file_list = glob.glob(os.path.join(self._lectures_folder, '*'))
        if file_list:
            oldest_file = min(file_list, key=os.path.getctime)
        self.__front = oldest_file
        return self.__front

    def pop(self):
        if self.__front and os.path.exists(self.__front):
            os.remove(self.__front)
            self.receive()
