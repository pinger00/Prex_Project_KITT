from flask import request, redirect, url_for, session, render_template
# Importar la contraseña desde prex_config
from app.prex_config import ADMIN_PASSWORD
from .debug import logger

# Ruta de autenticación para iniciar sesión


def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:  # Utilizar la variable .env
            session['logged_in'] = True
            logger.info('login correcto')
            return redirect(url_for('index'))
        else:
            logger.info('ande vas hacker, password incorrecto')
            return render_template('login.html', error='Contraseña incorrecta.')
    return render_template('login.html')

# Función que se ejecuta antes de cada request, verifica si está logueado


def before_request():
    if request.endpoint in ['index', 'ask_prex', 'ejecutar_comando'] and not session.get('logged_in'):
        return redirect(url_for('login'))
