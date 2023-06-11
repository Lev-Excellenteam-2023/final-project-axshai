from dataclasses import dataclass

import requests
from datetime import datetime


@dataclass
class Status:
    status: str
    filename: str
    timestamp: datetime
    explanation: list[str]

    def is_done(self):
        return self.status == 'done'


class WebClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def upload(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                response = requests.post(f"{self.base_url}/upload", files={'file': file})
                response_json = response.json()
                if response.ok:
                    return response_json['uid']
                else:
                    raise Exception(f"Upload failed: {response_json.get('error')}")
        except Exception as e:
            raise Exception(f"Upload failed: {str(e)}")

    def get_status(self, uid):
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
                raise Exception(f"Status request failed: {response_json.get('error')}")
        except Exception as e:
            raise Exception(f"Status request failed: {str(e)}")

