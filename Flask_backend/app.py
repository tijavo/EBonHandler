from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from EBonParser.rewebon import parse_rewe_bon

app = Flask(__name__)

# Konfiguration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Upload-Ordner erstellen falls nicht vorhanden
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    # Prüfen ob eine Datei im Request ist
    if 'file' not in request.files:
        return jsonify({'error': 'Keine Datei im Request'}), 400
    
    file = request.files['file']
    
    # Prüfen ob eine Datei ausgewählt wurde
    if file.filename == '':
        return jsonify({'error': 'Keine Datei ausgewählt'}), 400
    
    # Prüfen ob es eine PDF-Datei ist
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        json = parse_rewe_bon(filepath)
        
        return jsonify({
            'message': 'PDF erfolgreich hochgeladen',
            'filename': filename,
            'filepath': filepath,
            'data': json
        }), 200
    
    return jsonify({'error': 'Nur PDF-Dateien sind erlaubt'}), 400

@app.route('/', methods=['GET'])
def index():
    return '''
    <h2>PDF Upload</h2>
    <form method="POST" action="/upload-pdf" enctype="multipart/form-data">
        <input type="file" name="file" accept=".pdf">
        <input type="submit" value="Upload PDF">
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)