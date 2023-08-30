from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import os
import json

from werkzeug.utils import secure_filename

from web_api.web_helpers import _get_explanation_from_json_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(__file__, "..", "..", "uploads")
app.config['OUTPUTS_FOLDER'] = os.path.join(__file__, "..", "..", "outputs")


class RequestStatus:
    DONE = "done"
    PENDING = 'pending'
    NOT_FOUND = "not found"


@app.route('/upload', methods=['POST'])
def upload():
    """
    Handle file upload.

    This endpoint receives a file in a POST request and saves it in the uploads folder.
    It returns a JSON object with a unique identifier (UID) for the uploaded file.

    :return: JSON response with the UID of the upload.
    """
    if not os.path.isdir(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])

    if 'file' not in request.files:
        return jsonify({'error': 'No file provided.'}), 400

    file = request.files['file']
    uid = str(uuid.uuid4())

    original_base_filename, original_file_type = _get_lecture_name_and_type(secure_filename(file.filename))
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    new_filename = f"{original_base_filename}_{timestamp}_{uid}.{original_file_type}"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
    return jsonify({'uid': uid})


@app.route('/status/<uid>', methods=['GET'])
def status(uid: str):
    """
    Get the status of a request by UID.

    This endpoint returns the status of a request by the provided UID.
    If the request is done, it also returns the explanation.

    :param uid: The unique identifier (UID) of the request.
    :return: JSON response with the status and explanation (if available).
    """
    folder, file_name = _search_for_uid_in_folders([app.config['UPLOAD_FOLDER'], app.config['OUTPUTS_FOLDER']], uid)
    if file_name:
        if folder == app.config['OUTPUTS_FOLDER']:
            req_status = RequestStatus.DONE
            explanation = _get_explanation_from_json_file(os.path.join(folder, file_name))
        else:
            req_status = RequestStatus.PENDING
            explanation = None
        original_filename, timestamp, _ = file_name.split('_')
        return jsonify({
            'status': req_status,
            'filename': original_filename,
            'timestamp': timestamp,
            'explanation': explanation
        }), 200
    else:
        return jsonify({'status': RequestStatus.NOT_FOUND}), 404


def _search_for_uid_in_folders(folders_path: list[str], uid: str) -> tuple[str, str]:
    """
    Search for a UID in a list of folders.

    :param folders_path: List of folder paths to search.
    :param uid: The unique identifier (UID) to search for.
    :return: The folder and file name where the UID is found, or (None, None) if not found.
    """
    for folder in folders_path:
        if os.path.isdir(folder):
            file_list = os.listdir(folder)
            for filename in file_list:
                if os.path.isfile(os.path.join(folder, filename)) and uid in filename:
                    return folder, filename
    return "", ""


def _get_lecture_name_and_type(lecture_name: str) -> tuple[str, str]:
    """
    Extracts the lecture name and type from the lecture path.

    :param lecture_name: The path to the lecture file.
    :return: A tuple containing the lecture name and type.
    """
    return tuple(os.path.basename(lecture_name).split("."))


def run_web_server():
    """
    Run the Flask web server.

    This function starts the Flask web server to handle incoming requests.

    """
    app.run()
