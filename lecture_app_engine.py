import json
import os
import asyncio
import sys

from dotenv import dotenv_values

import openai_client
from lecture_parser import lecture_factory

WINDOWS_PLATFORM = 'win'


class AppEngine:
    ENV_FILE_PATH = ".env"
    OPENAI_API_KEY = "OPENAI_API_KEY"

    def __init__(self, lecture_path: str, destination_path: str):
        """
        Initializes an instance of the AppEngine class.

        :param lecture_path: The path to the lecture file.
        :param destination_path: The path to the directory where the explained lecture will be saved.
                                 If not provided, the same directory as the lecture file will be used.
        """
        self._lecture_name, lecture_type = self._get_lecture_name_and_type(lecture_path)
        self._parser = lecture_factory(lecture_type)(lecture_path)
        self._destination_path = destination_path if destination_path else os.path.dirname(lecture_path)

        # see https://stackoverflow.com/questions/63860576/asyncio-event-loop-is-closed-when-using-asyncio-run
        if sys.platform.startswith(WINDOWS_PLATFORM):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    def run_app(self):
        """
        Runs the application to explain the lecture and save the explained parts.
        """
        explained_parts = asyncio.run(self._explain_lecture())
        self._save_explained_lecture(explained_parts)

    async def _explain_lecture(self):
        """
        Processes each lecture part and retrieves explanations using the OpenAI model.

        :return: A list of explanations for each lecture part.
        """
        explained_lecture_parts = []
        api_key = dotenv_values(self.ENV_FILE_PATH)[self.OPENAI_API_KEY]
        client = openai_client.OpenAiClient(api_key)

        async def process_part(index: int, part):
            try:
                text_of_lec_part = self._parser.parse_lecture_part(part)
                if text_of_lec_part:
                    part_explanation = await client.get_slide_explanation(text_of_lec_part)
                    explained_lecture_parts.append((index, part_explanation))
            except Exception as e:
                part_explanation = f"An error occurred during processing this part: {str(e)}"
                explained_lecture_parts.append((index, part_explanation))

        lecture_parts = self._parser.get_lecture_parts()
        await asyncio.gather(*[process_part(index, part) for index, part in enumerate(lecture_parts)])

        # since we can't know which slide process is done first, we need
        # to sort the slides according to their original order:
        explained_lecture_parts.sort(key=lambda item: item[0])
        return [item[1] for item in explained_lecture_parts]

    def _save_explained_lecture(self, explained_lecture_parts: list[str]):
        """
        Saves the explained lecture parts to a JSON file.

        :param explained_lecture_parts: The list of explained lecture parts.
        """
        file_path = os.path.join(self._destination_path, self._lecture_name + ".json")
        with open(file_path, 'w') as json_file:
            json.dump(explained_lecture_parts, json_file)

    @staticmethod
    def _get_lecture_name_and_type(lecture_path: str) -> tuple[str, str]:
        """
        Extracts the lecture name and type from the lecture path.

        :param lecture_path: The path to the lecture file.
        :return: A tuple containing the lecture name and type.
        """
        return tuple(os.path.basename(lecture_path).split("."))
