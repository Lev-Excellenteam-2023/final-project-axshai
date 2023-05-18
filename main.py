import argparse
import os
import openai_client
from dotenv import dotenv_values
from lecture_parser import lecture_factory
ENV_FILE_PATH = ".env"
OPENAI_API_KEY = "OPENAI_API_KEY"


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--lecture_path",
                        help="the path to the lecture that should to be explained",
                        required=True)
    parser.add_argument("-d", "--destination_path",
                        help="The path to save the file containing the lesson explanation."
                             "(if not provided, the file will be saved in the same location of the lecture.)",
                        default="")
    return parser.parse_args()


def _get_lecture_name_and_type(lecture_path: str) -> tuple[str, str]:
    return tuple(os.path.basename(lecture_path).split("."))


def explain_lecture(lecture_parser):
    explained_lecture_parts = []
    api_key = dotenv_values(ENV_FILE_PATH)[OPENAI_API_KEY]
    client = openai_client.OpenAiClient(api_key)

    for part in lecture_parser.get_lecture_parts():
        try:
            text_of_lec_part = lecture_parser.parse_lecture_part(part)
            part_explanation = client.get_slide_explanation(text_of_lec_part)
        except Exception as e:
            part_explanation = f"An error occurred during Processing this part: {str(e)}"
        finally:
            if part_explanation:
                explained_lecture_parts.append(part_explanation)

    return explained_lecture_parts


def main():
    args = _parse_args()
    lecture_name, lecture_type = _get_lecture_name_and_type(args.lecture_path)
    lecture_parser = lecture_factory(lecture_type)
    explained_lecture_parts = explain_lecture(lecture_parser)


if __name__ == "__main__":
    main()
