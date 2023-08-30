import json


def _get_explanation_from_json_file(file_path: str) -> list[str]:
    """
    Get the explanation from a JSON file.

    :param file_path: Path to the JSON file.
    :return: The explanation from the JSON file.
    """
    with open(file_path, 'r') as output_file:
        explanation = json.load(output_file)
        return explanation["explained slides"]