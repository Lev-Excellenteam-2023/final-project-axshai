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

    server_thread = threading.Thread(target=web_server.run_web_server)
    server_thread.start()
    # Wait for the server to start
    time.sleep(2)
    explainer_thread = threading.Thread(target=run_explainer)
    explainer_thread.start()
    # Wait for the explainer to start
    time.sleep(2)
    web_client = WebClient("http://localhost:5000")
    uid = web_client.upload("asyncio-intro.pptx")
    # Wait for the explainer to finish his lecture processing
    time.sleep(34)
    response = web_client.get_status(uid)
    assert response.is_done(), "Test Failed!!\n" \
                               "Something went wrong - the process of explaining the lecture did not finished"
    print("Test Passed!!")


if __name__ == "__main__":
    run_test()
