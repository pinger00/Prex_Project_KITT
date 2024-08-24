import sys
import os

# Agregar el directorio principal del proyecto a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # noqa: E402

# Ahora realiza las importaciones
from app.prex_utils import *
from app.prex_command_detection import detect_command
from app.prex_commands import *  # Importar todos los comandos
from app.prex_auth import login, before_request  # Importar la autenticación
from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, session
from app.cert_manager import load_certificates
from app.prex_routes import *
import hashlib

# Inicializar la aplicación Flask
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'

# Rutas principales, incluyendo las de autenticación que importamos de prex_auth
app.route('/login', methods=['GET', 'POST'])(login)
app.before_request(before_request)

# Ruta para la página de inicio


@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')


# Registrar las rutas de Prex
register_prex_routes(app)


# Ruta para servir archivos de audio generados


@app.route('/audio/<path:filename>', methods=['GET'])
def serve_audio(filename):
    root_dir = os.path.abspath(os.path.dirname(__file__))
    return send_from_directory(os.path.join(root_dir, 'audio'), filename)

# Ruta para servir archivos estáticos


@app.route('/static/<path:filename>', methods=['GET'])
def serve_static(filename):
    root_dir = os.path.abspath(os.path.dirname(__file__))
    return send_from_directory(os.path.join(root_dir, 'static'), filename)


@app.route('/audio/temp/<filename>', methods=['GET'])
def serve_tmp_audio(filename):
    root_dir = os.path.abspath(os.path.dirname(__file__))
    return send_from_directory(os.path.join(root_dir, 'audio', 'temp'), filename)

# Ruta para favicon


@app.route('/favicon.ico')
def favicon():
    root_dir = os.path.abspath(os.path.dirname(__file__))
    return send_from_directory(os.path.join(root_dir, 'static'), 'favicon.ico')


# Crear carpetas necesarias si no existen
if not os.path.exists('temp'):
    os.makedirs('temp')
if not os.path.exists('static'):
    os.makedirs('static')
if not os.path.exists('templates'):
    os.makedirs('templates')

if __name__ == '__main__':
    # from main import app  # Importar la aplicación Flask desde el archivo main.py

    cert, key = load_certificates()
    app.logger.info('Starting application with SSL')
    app.run(host='0.0.0.0', port=443, ssl_context=(cert, key))
