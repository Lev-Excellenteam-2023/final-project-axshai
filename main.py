import argparse

from lecture_app_engine import AppEngine


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
    app_runner = AppEngine(args.lecture_path, args.destination_path)
    app_runner.run_app()


if __name__ == "__main__":
    import time

    # Start timer
    start_time = time.time()

    main()

    # End timer
    end_time = time.time()

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)
