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


