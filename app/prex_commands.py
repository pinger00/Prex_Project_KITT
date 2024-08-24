import requests
# Importar las credenciales desde prex_config
from app.prex_config import *
from .debug import logger
import hashlib


# Iniciar la recarga del coche


def start_charging():
    url = f"https://api.tessie.com/{vin}/command/start_charging"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {tessie_api_key}"
    }
    response = requests.post(url, headers=headers)
    return response.json()

# Detener la recarga del coche


def stop_charging():
    url = f"https://api.tessie.com/{vin}/command/stop_charging"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {tessie_api_key}"
    }
    response = requests.post(url, headers=headers)
    return response.json()

# Abrir el coche


def unlock_car():
    url = f"https://api.tessie.com/{vin}/command/unlock"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {tessie_api_key}"
    }
    response = requests.post(url, headers=headers)
    return response.json()

# Cerrar el coche


def lock_car():
    url = f"https://api.tessie.com/{vin}/command/lock"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {tessie_api_key}"
    }
    response = requests.post(url, headers=headers)
    return response.json()

# Abrir el puerto de carga


def open_charge_port():
    url = f"https://api.tessie.com/{vin}/command/open_charge_port"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {tessie_api_key}"
    }
    response = requests.post(url, headers=headers)
    return response.json()

# Activar el maletero trasero


def activate_rear_trunk():
    url = f"https://api.tessie.com/{vin}/command/activate_rear_trunk"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {tessie_api_key}"
    }
    response = requests.post(url, headers=headers)
    return response.json()

# Destellar las luces


def flash_lights():
    url = f"https://api.tessie.com/{vin}/command/flash"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {tessie_api_key}"
    }
    response = requests.post(url, headers=headers)
    return response.json()

# Tocar la bocina


def honk_horn():
    url = f"https://api.tessie.com/{vin}/command/honk"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {tessie_api_key}"
    }
    response = requests.post(url, headers=headers)
    return response.json()

# Ver el clima actual del coche


def get_weather():
    url = f"https://api.tessie.com/{vin}/weather"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {tessie_api_key}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Configurar la temperatura del conductor y del pasajero


def set_temperatures(driver_temp, passenger_temp):
    url = f"https://api.tessie.com/{vin}/command/set_temps"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {tessie_api_key}"
    }
    payload = {
        "driver_temp": driver_temp,
        "passenger_temp": passenger_temp
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Encender el clima


def start_climate():
    url = f"https://api.tessie.com/{vin}/command/start_climate"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {tessie_api_key}"
    }
    response = requests.post(url, headers=headers)
    return response.json()

# Apagar el clima


def stop_climate():
    url = f"https://api.tessie.com/{vin}/command/stop_climate"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {tessie_api_key}"
    }
    response = requests.post(url, headers=headers)
    return response.json()


def get_car_location():
    url = f"https://api.tessie.com/{vin}/location"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {tessie_api_key}"
    }
    response = requests.get(url, headers=headers)
    logger.info('Car location retrieved: %s', response.json())
    return response.json()


def get_battery_percentage():
    url = f"https://api.tessie.com/{vin}/battery"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {tessie_api_key}"
    }
    response = requests.get(url, headers=headers)
    logger.info('Battery percentage retrieved: %s', response.json())
    return response.json()


def get_battery_range():
    url = f"https://api.tessie.com/{vin}/range"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {tessie_api_key}"
    }
    response = requests.get(url, headers=headers)
    logger.info('Battery range retrieved: %s', response.json())
    return response.json()


def share_to_car(content):
    url = f"https: // api.tessie.com/{
        vin}/command/share?retry_duration = 40 & wait_for_completion = true & locale = en-US"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {tessie_api_key}"
    }
    payload = {
        "content": content
    }
    response = requests.post(url, headers=headers, json=payload)
    logger.info('Content shared to car: %s', response.json())
    return response.json()


# def generate_audio_response(answer, question):
#    try:
#        url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'
#        headers = {
#            'accept': 'audio/mpeg',
#            'xi-api-key': eleven_labs_api_key,
#            'Content-Type': 'application/json'
#        }
#        payload = {
#            'text': answer,
#            'model_id': 'eleven_multilingual_v2',
#            'voice_settings': {
#                'stability': 0.75,
#                'similarity_boost': 0.75
#            },
#            'language_id': 'es-ES'
#        }
#        audio_response = requests.post(url, json=payload, headers=headers)
#        if (audio_response.status_code != 200):
#            logger.error('Error generating audio response: %s',
#                         audio_response.status_code)
#            return None
#
 #       audio_filename = f'output_{hashlib.md5(
#            question.encode()).hexdigest()}.mp3'
#        audio_path = os.path.join('temp', audio_filename)
#        with open(audio_path, 'wb') as audio_file:
#            audio_file.write(audio_response.content)
#        logger.info(
#            'Audio response generated successfully: %s', audio_filename)
#        return audio_filename
#    except Exception as e:
#        logger.error('Error generating audio response: %s', e)
#        return None
