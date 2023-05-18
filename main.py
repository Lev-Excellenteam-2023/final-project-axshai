import argparse
import os
from lecture_parser import lecture_factory


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
def main():
    args = _parse_args()
    lecture_name, lecture_type = _get_lecture_name_and_type(args.lecture_path)
    lecture_parser = lecture_factory(lecture_type)


if __name__ == "__main__":
    main()
