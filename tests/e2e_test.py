import os
import threading
import time

import web_api.web_app as web_server
from explainer.explainer_pip_client import run_explainer
from web_client.web_client import WebClient


def run_test():
    """
    Run the test scenario.

    This function starts the web server and the explainer in separate threads, performs an upload, waits for the
    explainer to finish processing the lecture, and retrieves the status. It then asserts that the process of
    explaining the lecture is done and prints the test result.
    """

    print("starting web api")
    start_server()

    # Wait for the server to start
    time.sleep(2)
    print("starting explainer")
    start_explainer()

    # Wait for the explainer to start
    time.sleep(2)
    web_client = WebClient("http://localhost:5000")
    uid = web_client.upload("asyncio-intro.pptx")
    # Wait for the explainer to finish his lecture processing
    print("going to sleep to 34 seconds to for the explainer to finish his lecture processing")
    time.sleep(34)
    response = web_client.get_status(uid)
    assert response.is_done(), f"Test Failed!!\n" \
                               f"expected status was done, got {response.status}"
    print("Test Passed!!")


def start_explainer():
    explainer_thread = threading.Thread(target=run_explainer)
    explainer_thread.daemon = True
    explainer_thread.start()


def start_server():
    server_thread = threading.Thread(target=web_server.run_web_server)
    server_thread.daemon = True
    server_thread.start()


if __name__ == "__main__":
    run_test()
