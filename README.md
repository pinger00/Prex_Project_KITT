
# PREX - Proyecto Robótico Eléctrico X

## Descripción
Este proyecto representa el sistema PREX (Proyecto Robótico Eléctrico X), inspirado en el famoso KITT de la serie "Knight Rider". Se trata de un sistema integrado en un vehículo eléctrico que permite ejecutar comandos, con una personalidad propia basada en humor y asistencia.

## Instalación
1. Clona el repositorio en tu máquina local:
   ```
   git clone https://github.com/tu_proyecto/prex.git
   ```

2. Instala las dependencias necesarias:
   ```
   pip install -r requirements.txt
   ```

3. Crea un archivo `.env` en la raíz del proyecto (usa el archivo `.env.example` como referencia) y agrega tus claves API y variables de entorno.

4. Si tienes un certificado SSL, colócalo en el directorio correspondiente y asegúrate de configurar el servidor con SSL activado.

## Ejecutar el Proyecto
Para ejecutar el proyecto en modo desarrollo con soporte HTTPS:
   ```
   python app/main.py
   ```

## Configuración del Certificado SSL
Para ejecutar la aplicación sobre HTTPS, asegúrate de tener tu certificado (`cert.pem`) y clave privada (`key.pem`) listos. Flask puede manejar HTTPS directamente en desarrollo de la siguiente manera:
   ```python
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
   ```

Para servidores de producción (como Nginx), configura el certificado SSL en el servidor, no en Flask.

## Comandos
El archivo `commands.py` te permitirá agregar fácilmente nuevos comandos que PREX puede ejecutar. Ya vienen configurados algunos comandos básicos como:
   - `start`: Inicia el sistema PREX.
   - `stop`: Detiene el sistema.
   - `check_status`: Verifica el estado del sistema.

Para agregar nuevos comandos, simplemente edita el archivo `commands.py`.

## Seguridad
1. Asegúrate de que el archivo `.env` no sea accesible desde el servidor. El proyecto está configurado para que no se sirva nunca este archivo.
2. Recomendamos servir la aplicación solo bajo HTTPS para asegurar la transmisión de datos.

## ¡Disfruta de PREX!
