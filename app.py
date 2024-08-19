from flask import Flask, request, redirect, url_for, send_from_directory, render_template
import os

app = Flask(__name__)

# Définir le dossier pour stocker les fichiers téléchargés
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def format_size(size_in_bytes):
    if size_in_bytes < 1024 * 1024:
        return f"{round(size_in_bytes / 1024, 2)} KB"
    else:
        return f"{round(size_in_bytes / (1024 * 1024), 2)} MB"

@app.route('/')
def index():
    # Liste des fichiers disponibles dans le dossier d'upload avec leur taille formatée
    files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file_size = os.path.getsize(filepath)
        formatted_size = format_size(file_size)
        files.append({'name': filename, 'size': formatted_size})
    
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
