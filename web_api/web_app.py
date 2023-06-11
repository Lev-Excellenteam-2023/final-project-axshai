from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import os
import json

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(__file__, "..", "uploads")
app.config['OUTPUTS_FOLDER'] = os.path.join(__file__, "..", "outputs")


class RequestStatus:
    DONE = "done"
    PENDING = 'pending'
    NOT_FOUND = "not found"


@app.route('/upload', methods=['POST'])
def upload():
    if not os.path.isdir(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])

    # Check if a file was sent in the POST request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided.'}), 400

    file = request.files['file']

    # Generate a UID for the uploaded file
    uid = str(uuid.uuid4())

    # Get the original filename and timestamp
    original_filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # Create a new filename combining original filename, timestamp, and UID
    new_filename = f"{original_filename}_{timestamp}_{uid}"

    # Save the file in the uploads folder
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

    # Return a JSON object with the UID of the upload
    return jsonify({'uid': uid})


def _get_explanation_from_json_file(file_path):
    with open(file_path, 'r') as output_file:
        explanation = json.load(output_file)["explained slides"]
        return explanation


@app.route('/status/<uid>', methods=['GET'])
def status(uid):
    folder, file_name = _search_for_uid_in_folders(app.config['UPLOAD_FOLDER'], app.config['OUTPUTS_FOLDER'])
    if file_name:
        if folder == app.config['OUTPUTS_FOLDER']:
            req_status = RequestStatus.DONE
            explanation = _get_explanation_from_json_file(os.path.join(folder, file_name))
        else:
            req_status = RequestStatus.PENDING
            explanation = None
        timestamp, _, original_filename = file_name.split('_')[:3]
        return jsonify({
            'status': req_status,
            'filename': original_filename,
            'timestamp': timestamp,
            'explanation': explanation
        }), 200
    else:
        return jsonify({'status': RequestStatus.NOT_FOUND}), 404


def _search_for_uid_in_folders(folders_path, uid):
    for folder in folders_path:
        if os.path.isdir(folder):
            file_list = os.listdir(folder)
            for filename in file_list:
                if os.path.isfile(filename) and uid in filename:
                    return folder, filename


if __name__ == '__main__':
    app.run()
