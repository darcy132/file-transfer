from flask import Flask, request, send_file, render_template, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
BASE_FOLDER = 'server_files'  # Base directory for server files

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['BASE_FOLDER'] = BASE_FOLDER

# Ensure the upload and base folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(BASE_FOLDER, exist_ok=True)

@app.route('/')
@app.route('/browse/')
def index():
    # List files and directories in the base folder
    return list_directory('')

@app.route('/browse/<path:subpath>')
def browse_directory(subpath):
    # List files and directories in the specified subpath
    return list_directory(subpath)

def list_directory(subpath):
    # Construct the full path
    full_path = os.path.join(app.config['BASE_FOLDER'], subpath)
    if not os.path.exists(full_path):
        return 'Directory not found', 404

    # List files and directories
    items = os.listdir(full_path)
    files = []
    dirs = []
    for item in items:
        item_path = os.path.join(full_path, item)
        if os.path.isfile(item_path):
            files.append(item)
        elif os.path.isdir(item_path):
            dirs.append(item)

      # Calculate the parent directory
    if subpath:
        parent_path = os.path.dirname(subpath)
        if parent_path == subpath:  # Root directory case
            parent_path = ''
    else:
        parent_path = ''
         
    # Render the template with the list of files and directories
    return render_template('index.html', files=files, dirs=dirs, current_path=subpath, os=os, parent_path=parent_path)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return 'File uploaded successfully', 200

@app.route('/download/<path:filename>')
def download_file(filename):
    # Construct the full path to the file
    full_path = os.path.join(app.config['BASE_FOLDER'], filename)
    if os.path.isfile(full_path):
        return send_file(full_path, as_attachment=True)
    return 'File not found', 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')