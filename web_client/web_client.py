from dataclasses import dataclass

import requests
from datetime import datetime

from web_api.web_app import RequestStatus


@dataclass
class Status:
    """
    Represents the status of a request.

    This data class holds the status, filename, timestamp, and explanation of a request.

    :param status: The status of the request.
    :param filename: The filename associated with the request.
    :param timestamp: The timestamp of the request.
    :param explanation: The explanation associated with the request.
    """
    status: str
    filename: str
    timestamp: datetime
    explanation: list[str]

    def is_done(self) -> bool:
        """
        Check if the request status is done.

        :return: True if the request status is done, False otherwise.
        """
        return self.status == 'done'


class WebClient:
    def __init__(self, base_url: str):
        """
        Initialize the WebClient.

        :param base_url: The base URL of the web server.
        """
        self.base_url = base_url

    def upload(self, file_path: str, email: str = None) -> str:
        """
        Upload a file to the web server.

        :param email: (Optional) The email address to associate with the upload.
        :param file_path: The path to the file to upload.
        :return: The UID of the uploaded file.
        :raises Exception: If the upload fails.
        """
        try:
            with open(file_path, 'rb') as file:
                files = {'file': file}
                data = {"email": email} if email else None
                response = requests.post(f"{self.base_url}/upload", files=files, data=data)
                response_json = response.json()
                if response.ok:
                    return response_json['uid']
                else:
                    raise Exception(f"Upload failed: {response_json.get('error')}")
        except Exception as e:
            raise Exception(f"Upload failed: {str(e)}")

    def get_status(self, uid: str) -> Status:
        """
        Get the status of a request by UID.

        :param uid: The unique identifier (UID) of the request.
        :return: Status Object representing the status of the request.
        :raises Exception: If the status request fails.
        """
        try:
            response = requests.get(f"{self.base_url}/status/{uid}")
            response_json = response.json()
            if response.ok:
                status = response_json['status']
                filename = response_json['filename']
                timestamp = response_json['timestamp']
                explanation = response_json['explanation']
                return Status(status, filename, timestamp, explanation)
            else:
                raise Exception(f"Status request failed: {response_json.get('status')}")
        except Exception as e:
            raise Exception(f"Status request failed: {str(e)}")
