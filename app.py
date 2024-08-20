from flask import Flask, request, redirect, url_for, send_from_directory, render_template
# import logging
from waitress import serve
import os
import socket

app = Flask(__name__)

# Codes de couleurs ANSI
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Désactivez l'avertissement en modifiant le niveau de journalisation de Flask
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

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
    host = '0.0.0.0'
    port = 5000
    message = f"""{YELLOW}

██╗  ██╗███████╗██████╗ ██╗    ███████╗ ██████╗ ███████╗████████╗
██║  ██║██╔════╝██╔══██╗██║    ██╔════╝██╔═══██╗██╔════╝╚══██╔══╝
███████║█████╗  ██████╔╝██║    ███████╗██║   ██║█████╗     ██║   
██╔══██║██╔══╝  ██╔══██╗██║    ╚════██║██║   ██║██╔══╝     ██║   
██║  ██║███████╗██║  ██║██║    ███████║╚██████╔╝██║        ██║   
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝    ╚══════╝ ╚═════╝ ╚═╝        ╚═╝   
***********Développée par Herimalala VALISOA*********************
    {RESET}                                                           
    """
    # Obtenir l'adresse IP locale
    local_ip = socket.gethostbyname(socket.gethostname())
    
    # Affiche un message dans le terminal avant de lancer l'application
    print(message)
    print(f"L'application Flask est accessible sur {GREEN}http://{local_ip}:{port}")
    print(f"{RED}Appuyer sur ctrl+c pour quitter...{RESET}")

    serve(app, host=host, port=port)
    
    # serveur pour developpement
    # app.run(debug=False, host='0.0.0.0', port=5000)
