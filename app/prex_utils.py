import os
import hashlib
import requests
# Importar claves de API
from app.prex_config import *

# Obtener la zona horaria a partir de la latitud y longitud


def get_timezone_by_location(latitude, longitude):
    url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={
        TIMEZONEDB_API_KEY}&format=json&by=position&lat={latitude}&lng={longitude}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("zoneName")
    else:
        return None

# Obtener la hora actual en la zona horaria proporcionada


def get_current_time(timezone):
    url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={TIMEZONEDB_API_KEY}&format=json&by=zone&zone={
        timezone}"
    response = requests.get(url)
    if response.status_code == 200:
        datetime_info = response.json().get("formatted")
        return datetime_info
    else:
        return None

# Buscar lugares cercanos a una ubicación (latitud, longitud) usando Google Places API


def find_nearby_places(latitude, longitude, keyword):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={
        latitude},{longitude}&radius=5000&keyword={keyword}&key={google_places_api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        places = response.json().get('results', [])
        if places:
            locations = []
            for place in places:
                name = place.get('name')
                address = place.get('vicinity')
                locations.append(f"{name}, {address}")
            return locations
        else:
            return [f"No se encontraron lugares cercanos para: {keyword}."]
    else:
        return [f"Error al buscar lugares cercanos para: {keyword}."]

# Generar un archivo de audio a partir de la respuesta de Prex usando Eleven Labs API


def generate_audio_response(answer, question):
    try:
        url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'
        headers = {
            'accept': 'audio/mpeg',
            'xi-api-key': eleven_labs_api_key,
            'Content-Type': 'application/json'
        }
        payload = {
            'text': answer,
            'model_id': 'eleven_multilingual_v2',
            'voice_settings': {
                'stability': 0.75,
                'similarity_boost': 0.75
            },
            'language_id': 'es-ES'
        }
        audio_response = requests.post(url, json=payload, headers=headers)
        if audio_response.status_code != 200:
            return None

        audio_filename = f'output_{hashlib.md5(
            question.encode()).hexdigest()}.mp3'
        audio_path = os.path.join('app', 'audio', 'temp', audio_filename)
        with open(audio_path, 'wb') as audio_file:
            audio_file.write(audio_response.content)
        return audio_filename
    except Exception as e:
        return None
