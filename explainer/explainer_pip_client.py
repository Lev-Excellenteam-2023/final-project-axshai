import os
import time

from explainer.explainer_pipe_interface import FileSystemPipe

POLL_INTERVAL = 10
UPLOADS_DIR = os.path.join(__file__, "..", "uploads")
OUTPUTS_FOLDER = os.path.join(__file__, "..", "outputs")


def main():

    pipe = FileSystemPipe(UPLOADS_DIR, OUTPUTS_FOLDER)
    while True:
        while pipe.receive():
            lecture_to_explain = pipe.receive()
            print(f"{lecture_to_explain} found in pipe")
            pipe.send(lecture_to_explain)
            print(f"explained {lecture_to_explain} saved into the output directory")
            pipe.pop()
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
