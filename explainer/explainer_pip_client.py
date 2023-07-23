import os
import time

from explainer.explainer_pipe_interface import DataBasePipe

POLL_INTERVAL = 10
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
OUTPUTS_FOLDER = os.path.join(os.path.dirname(__file__), "..", "outputs")


def run_explainer():
    """
      Run the explainer process.

      This function continuously checks for lectures in the pipe, explains them,
      and saves the results in the output directory.
      """

    pipe = DataBasePipe(UPLOADS_DIR, OUTPUTS_FOLDER)
    while True:
        while pipe.receive():
            lecture_to_explain = pipe.receive()
            print(f"{lecture_to_explain} found in pipe")
            pipe.send(lecture_to_explain)
            print(f"explained {lecture_to_explain} saved into the output directory")
            pipe.pop()
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    run_explainer()
