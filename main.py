from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import tensorflow_judger
import token_manager
import os
import secrets
import string

if not os.path.exists('token_db'):
    os.makedirs('token_db')
if not os.path.exists('file_storage'):
    os.makedirs('file_storage')

app = Flask(__name__)

# setting max size of file
MAX_FILESIZE = 'your_max_filesize'
app.config['MAX_CONTENT_LENGTH'] = MAX_FILESIZE

TOKEN_PREFIX = 'your_token_prefix'
token_verify = token_manager.TokenManager('token_db/tokens.db')

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'score': 0.0, 'status': 'error', 'message': f'File size should not exceed {MAX_FILESIZE / (1024 * 1024)} MB', 'user': 'Pre-production phase obstruction'}), 413

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'score': 0.0, 'status': 'error', 'message': 'Internal server error occurred', 'user': 'Pre-production phase obstruction'}), 500

def verify_access_token(token):
    return token_verify.verify_token(token)

def require_token(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith(TOKEN_PREFIX):
            return jsonify({'score': 0.0, 'status': 'error', 'message': 'Invalid or missing access token', 'user': 'Unable to identify'}), 401
        token = token.split(TOKEN_PREFIX)[1]
        user_id = verify_access_token(token)
        if not user_id:
            return jsonify({'score': 0.0, 'status': 'error', 'message': 'Invalid access token', 'user': 'Unable to identify'}), 401
        return func(user_id, *args, **kwargs)
    return wrapper

@app.route('/', methods=['POST'])
@require_token
def upload_file(user_id):
    # check if the file update
    if 'file' not in request.files:
        return jsonify({'score': 0.0, 'status': 'error', 'message': 'No file part', 'user': user_id})

    file = request.files['file']

    # check if the file is empity
    if file.filename == '':
        return jsonify({'score': 0.0, 'status': 'error', 'message': 'No selected file', 'user': user_id})

    # check if the file legal
    if file and allowed_file(file.filename):
        filename = './file_storage/' + str(user_id) + '_' + secure_filename(generate_random_string(32))
        file.save(filename)
        result = tensorflow_judger.judger(filename)
        return jsonify({'score': result, 'status': 'success', 'message': 'File uploaded successfully', 'user': user_id})

    return jsonify({'score': 0.0, 'status': 'error', 'message': 'File upload failed', 'user': user_id})

def allowed_file(filename):
    # check if file extention legal
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'h5'}

def generate_random_string(length):
    alphabet = string.ascii_letters
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == '__main__':
    app.run(threaded=True, host='localhost', port=80)