import uuid
from db_interface.tables import User, Upload
import db_interface.tables as db
from flask import Flask, request, jsonify
from datetime import datetime

import os
import json

from sqlalchemy import select
from sqlalchemy.orm import Session

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), "..", "uploads")
app.config['OUTPUTS_FOLDER'] = os.path.join(os.path.dirname(__file__), "..", "outputs")


class RequestStatus:
    DONE = "done"
    PENDING = 'pending'
    NOT_FOUND = "not found"
    PROCESSING = "Processing"


@app.route('/upload', methods=['POST'])
def upload():
    """
    Handle file upload.

    This endpoint receives a file in a POST request and saves it in the uploads folder.
    It returns a JSON object with a unique identifier (UID) for the uploaded file.

    :return: JSON response with the UID of the upload.
    """
    new_filename = None
    if not os.path.isdir(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])

    if 'file' not in request.files:
        return jsonify({'error': 'No file provided.'}), 400

    file = request.files['file']

    uid = uuid.uuid4()
    email = request.form.get('email')
    engine = db.get_engine()
    with Session(engine) as session:
        f_upload = Upload(uid=uid, filename=os.path.basename(file.filename),
                          upload_time=datetime.now(), status=RequestStatus.PENDING)
        new_filename = f_upload.upload_path(app.config['UPLOAD_FOLDER'])
        session.add(f_upload)
        session.commit()

        if email:
            user = _get_user_by_email(email, session)
            if not user:
                user = User(email=email)
            user.uploads.append(f_upload)
            f_upload.user = user
            f_upload.user_id = user.id
            session.add_all([user, f_upload])
            session.commit()

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
    return jsonify({'uid': str(uid)})


def _get_explanation_from_json_file(file_path: str) -> list[str]:
    """
    Get the explanation from a JSON file.

    :param file_path: Path to the JSON file.
    :return: The explanation from the JSON file.
    """
    with open(file_path, 'r') as output_file:
        explanation = json.load(output_file)
        return explanation["explained slides"]


@app.route('/status/<uid_or_filename>', methods=['GET'])
def status(uid_or_filename: str):
    """
    Get the status of a request by UID or filename with email.

    This endpoint returns the status of a request by the provided UID or filename with email.
    If the request is done, it also returns the UID, status, and finish time.

    :param uid_or_filename: The unique identifier (UID) of the request or the filename with email.
    :return: JSON response with the UID, status, and finish time (if available).
    """
    latest_upload = None
    if '@' in uid_or_filename:
        # If the parameter contains '@', it means it's a filename with email
        filename, email = uid_or_filename.split(' ')
        with Session(db.get_engine()) as session:
            user = _get_user_by_email(email, session)
            if user:
                latest_upload = _get_user_latest_upload(filename, user)
    else:
        # Otherwise, treat it as a UID
        latest_upload = _get_upload_by_uid(uid_or_filename)
    if latest_upload:
        response_code = 200
        upload_uid = latest_upload.uid
        response = {'uid': upload_uid,
                    'status': latest_upload.status,
                    'upload_time': latest_upload.upload_time.strftime('%Y-%m-%d-%H-%M-%S'),
                    'filename': latest_upload.filename}
        if latest_upload.status == RequestStatus.DONE:
            response['explanation'] = _get_explanation_from_json_file(
                latest_upload.output_path(base_path=app.config['OUTPUTS_FOLDER']))
            response['finish_time'] = latest_upload.finish_time.strftime('%Y-%m-%d-%H-%M-%S')
    else:
        response = {'status': RequestStatus.NOT_FOUND}
        response_code = 404
    return jsonify(response), response_code


def _get_user_by_email(email, session):
    select_statement = select(User).where(User.email == email)
    result = session.scalars(select_statement).all()
    if result:
        print("hiii result", result)
        return result[0]
    else:
        return None


def _get_user_latest_upload(filename, user: User):
    latest_time = max([user_upload.upload_time for user_upload in user.uploads if user_upload.filename == filename])
    return [user_upload for user_upload in user.uploads if user_upload.filename == filename and
            user_upload.upload_time == latest_time][0]


def _get_upload_by_uid(str_uid) -> Upload:
    uid = uuid.UUID(str_uid)
    with Session(db.get_engine()) as session:
        select_statement = select(Upload).where(Upload.uid == uid)
        return session.scalars(select_statement).all()[0]


def run_web_server():
    """
    Run the Flask web server.

    This function starts the Flask web server to handle incoming requests.

    """
    app.run()
