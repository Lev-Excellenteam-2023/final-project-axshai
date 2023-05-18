import argparse


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


def main():
    args = _parse_args()


if __name__ == "__main__":
    main()
