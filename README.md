<h1 align="center"><em># Prex_Project_KITT </em></h1>

Este proyecto representa el sistema PREX (Proyecto Robótico Eléctrico X), inspirado en el famoso KITT de la serie "Knight Rider". Se trata de un sistema integrado en un vehículo eléctrico Tesla que permite ejecutar comandos, recibiendo feedback del coche, con una personalidad propia basada en humor y asistencia. Habla a tu coche y este te responderá en un tono similar a KITT, puedes pedirle abrir o cerrar el maletero, ver el nivel de batería, pitar, o abrir o cerrar el coche entre otros comandos y lo hará por tí.

Compatible con MCU2 con la app TeslaDisplay (https://tesladisplay.com/). 

![Manual_uso](https://github.com/user-attachments/assets/eec56b5a-fa73-4ca1-b213-e7ebec364629)

#  ADVERTENCIA !!!!
Este software se ha hecho a base de prueba y error, NO SOY PROGRAMADOR. No me hago responsable de los daños que este software pueda ocasionar. Se hizo en colaboración con varias IA's. Mayormente en ChatGPT, aunque también con ayuda de otros LLM's. 	

#REQUISITOS
Configura tu .env. Necesitarás las claves API's de mínimo Elevenlabs (cuenta gratuita), OpenAI (cuenta de pago). Necesitarás un servidor con capacidad para ejecutar código python (puede ser cualquier PC).

ADMIN_PASSWORD=your_admin_password
# Protege tu vehículo de usos no autorizados, consigue una contraseña lo más fuerte posible.

TESSIE_API_KEY=your_tessie_api_key              
# Imprescindible para comunicar con el vehiculo. Me puedes ayudar a pagar la suscripción a Tessie usando este enlace: https://share.tessie.com/nDAlwNM5LKb  Muchísimas grácias.

VIN=your_vehicle_identification_number          
# Lo puedes conseguir en la app de Tessie

ELEVEN_LABS_API_KEY=your_eleven_labs_api_key    
# Registrate en una cuenta de pago según tu uso

VOICE_ID=sTgnjW6Su298ryjA5cNd                   
# selecciona la voz desde elevenlabs, por defecto voz Prex

GOOGLE_PLACES_API_KEY=your_google_places_api_key 
# Registrate para tener acceso a google maps, gratis con un uso pequeño.

OPENAI_API_KEY=your_openai_api_key              
# Consigue tu KEY en openai

TIMEZONEDB_API_KEY=your_timezonedb_api_key      
# Consigue tu KEY en timezonedb, es gratis

Opcionales pero muy recomendables:
API TESSIE, link referido: https://share.tessie.com/nDAlwNM5LKb 
#IMPRESCINDIBLE para integración con el coche.

TIMEZONEDB 
# Para ver la hora local, útil si viajas y hay cambios horarios, la api key se puede conseguir gratis.
Google Places API - 
#Si se le da poco uso puedes registrate grátis.

REQUISITOS OPERATIVOS:
Python 3.8+
Flask
openai
requests
python-dotenv


## Instalación
1. Clona el repositorio en tu máquina local:
   ```
   git clone https://github.com/pinger00/Prex_Project_KITT
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
El archivo `commands.py` te permitirá agregar nuevos comandos que PREX puede ejecutar. Ya vienen configurados algunos comandos básicos como:
- "ver la ubicación del coche"
- "compartir dirección"
- "enviar dirección a navegador"
- "compartir vídeo"
- "ver batería"
- "ver kilómetros restantes"
- "ver hora local"
- "buscar X cercano"
- "buscar restaurante cercano"
- "buscar hotel cercano"
- "buscar punto de recarga cercano"
- "buscar supercharger cercano"
- "iniciar recarga"
- "parar recarga"
- "abrir coche"
- "cerrar coche"
- "abrir puerto de recarga"
- "tocar bocina"
- "pita"
- "abrir maletero"
- "cerrar maletero"
- "destellar luces"
- "ver el tiempo"
- "encender clima"
- "apagar clima"
- "poner temperatura a"

  No es necesario memorizarlos ya que puedes hablar normalmente y el sistema se encarga de detectar si es o no un comando y llamar al comando adecuado.

Para agregar nuevos comandos, edita el archivo `commands.py`. Puedes personalizar el nombre del coche en `prex_config.py` en la sección contexto. También podrás indicar tu modelo de coche para que sepa donde está. 

## Seguridad
1. Asegúrate de que el archivo `.env` no sea accesible desde el servidor. El proyecto está configurado para que no se sirva nunca este archivo.
2. Recomendamos servir la aplicación solo bajo HTTPS para asegurar la transmisión de datos.

## ¡Disfruta de PREX y no olvides conectar conmigo en X, usuario: iPhoneGamesDev !


******************************************************************************************
<h1 align="center"><em># Prex_Project_KITT </em></h1>

This project represents the PREX system (Proyecto Robótico Eléctrico X), inspired by the famous KITT from the "Knight Rider" series. It is an integrated system in a Tesla electric vehicle that allows executing commands, receiving feedback from the car, with its own personality based on humor and assistance. Talk to your car and it will respond in a tone similar to KITT, you can ask it to open or close the trunk, check the battery level, honk, or open or close the car among other commands and it will do it for you.

Commands and voice are in spanish, You can translate it if you want. You can use IA ;)

Compatible with MCU2 with the TeslaDisplay app (https://tesladisplay.com/).

![Manual_uso](https://github.com/user-attachments/assets/eec56b5a-fa73-4ca1-b213-e7ebec364629)

# WARNING !!!!
This software has been made through trial and error, I AM NOT A PROGRAMMER. I am not responsible for any damage this software may cause. It was made in collaboration with several AIs. Mostly in ChatGPT, but also with the help of other LLMs.

# REQUIREMENTS
Set up your .env. You will need API keys from at least Elevenlabs (free account), OpenAI (paid account). You will need a server capable of running python code (can be any PC).

ADMIN_PASSWORD=your_admin_password
# Protect your vehicle from unauthorized uses, get the strongest password possible.

TESSIE_API_KEY=your_tessie_api_key
# Essential for communicating with the vehicle. You can help me pay for the Tessie subscription using this link: https://share.tessie.com/nDAlwNM5LKb Thank you very much.

VIN=your_vehicle_identification_number
# You can get this in the Tessie app

ELEVEN_LABS_API_KEY=your_eleven_labs_api_key
# Sign up for a paid account according to your usage

VOICE_ID=sTgnjW6Su298ryjA5cNd
# select the voice from elevenlabs, default voice Prex

GOOGLE_PLACES_API_KEY=your_google_places_api_key
# Register to have access to google maps, free with small usage.

OPENAI_API_KEY=your_openai_api_key
# Get your KEY at openai

TIMEZONEDB_API_KEY=your_timezonedb_api_key
# Get your KEY at timezonedb, it's free

Optional but highly recommended:
TESSIE API, referral link: https://share.tessie.com/nDAlwNM5LKb
#ESSENTIAL for integration with the car.
TIMEZONEDB
# To check the local time, useful if you travel and there are timezone changes, the api key can be obtained for free.
Google Places API -
#If it is lightly used you can register for free.

OPERATIONAL REQUIREMENTS:
Python 3.8+
Flask
openai
requests
python-dotenv

## Installation
1. Clone the repository to your local machine:
git clone https://github.com/pinger00/Prex_Project_KITT

markdown
Copiar código

2. Install the necessary dependencies:
pip install -r requirements.txt

javascript
Copiar código

3. Create a `.env` file at the root of the project (use the `.env.example` file as a reference) and add your API keys and environment variables.

4. If you have an SSL certificate, place it in the appropriate directory and make sure to configure the server with SSL enabled.

## Running the Project
To run the project in development mode with HTTPS support:
python app/main.py

arduino
Copiar código

## SSL Certificate Configuration
To run the application over HTTPS, make sure you have your certificate (`cert.pem`) and private key (`key.pem`) ready. Flask can handle HTTPS directly in development as follows:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
For production servers (such as Nginx), configure the SSL certificate on the server, not in Flask.

Commands
The commands.py file will allow you to add new commands that PREX can execute. Some basic commands are already configured such as:

"see the location of the car"
"share address"
"send address to navigator"
"share video"
"check battery"
"check remaining kilometers"
"check local time"
"search for X nearby"
"search for a nearby restaurant"
"search for a nearby hotel"
"search for a nearby charging point"
"search for a nearby supercharger"
"start charging"
"stop charging"
"open car"
"close car"
"open charging port"
"honk horn"
"beep"
"open trunk"
"close trunk"
"flash lights"
"check the weather"
"turn on climate control"
"turn off climate control"
"set temperature to"
There is no need to memorize them as you can talk normally and the system will detect whether or not it is a command and call the appropriate command.

To add new commands, edit the commands.py file. You can customize the name of the car in prex_config.py in the context section. You can also indicate your car model so it knows where it is.

Security
Make sure the .env file is not accessible from the server. The project is set up so that this file is never served.
We recommend serving the application under HTTPS only to secure data transmission.
Enjoy PREX and don't forget to connect with me on X, user: iPhoneGamesDev!
