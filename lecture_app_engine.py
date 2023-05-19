import json
import os
from dotenv import dotenv_values

import openai_client
from lecture_parser import lecture_factory


class AppEngine:
    ENV_FILE_PATH = ".env"
    OPENAI_API_KEY = "OPENAI_API_KEY"

    def __init__(self, lecture_path, destination_path):
        self._lecture_name, lecture_type = self._get_lecture_name_and_type(lecture_path)
        self._parser = lecture_factory(lecture_type)
        self._destination_path = destination_path if destination_path else os.path.dirname(lecture_path)

    def run_app(self):
        self._explain_lecture()
        self._save_explained_lecture()

    def _explain_lecture(self):
        explained_lecture_parts = []
        api_key = dotenv_values(self.ENV_FILE_PATH)[self.OPENAI_API_KEY]
        client = openai_client.OpenAiClient(api_key)

        for part in self._parser.get_lecture_parts():
            try:
                text_of_lec_part = self._parser.parse_lecture_part(part)
                part_explanation = client.get_slide_explanation(text_of_lec_part)
            except Exception as e:
                part_explanation = f"An error occurred during Processing this part: {str(e)}"
            finally:
                if part_explanation:
                    explained_lecture_parts.append(part_explanation)

        return explained_lecture_parts

    def _save_explained_lecture(self, explained_lecture_parts):
        file_path = os.path.join(self._destination_path, self._lecture_name + ".json")
        with open(file_path, 'w') as json_file:
            json.dump(explained_lecture_parts, json_file)

    @staticmethod
    def _get_lecture_name_and_type(lecture_path: str) -> tuple[str, str]:
        return tuple(os.path.basename(lecture_path).split("."))
