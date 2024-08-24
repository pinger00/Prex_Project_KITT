# Prex_Project_KITT
Este proyecto representa el sistema PREX (Proyecto Robótico Eléctrico X), inspirado en el famoso KITT de la serie "Knight Rider". Se trata de un sistema integrado en un vehículo eléctrico Tesla que permite ejecutar comandos, con una personalidad propia basada en humor y asistencia. Compatible con MCU2 con la app TeslaDisplay (https://tesladisplay.com/). 
![Manual_uso](https://github.com/user-attachments/assets/eec56b5a-fa73-4ca1-b213-e7ebec364629)

#  ADVERTENCIA !!!!
Este software se ha hecho a base de prueba y error, NO SOY PROGRAMADOR. Se hizo en colaboración con varias IA's. Mayormente en ChatGPT, aunque también con ayuda de otros LLM's. 

#REQUISITOS
Configura tu .env. Necesitarás las claves API's de mínimo Elevenlabs (cuenta gratuita), OpenAI (cuenta de pago). Necesitarás un servidor con capacidad para ejecutar código python (puede ser cualquier PC).

ADMIN_PASSWORD=your_admin_password              # Protege tu vehículo de usos no autorizados
TESSIE_API_KEY=your_tessie_api_key              # Imprescindible para comunicar con el vehiculo 
VIN=your_vehicle_identification_number          # Lo puedes conseguir en la app de Tessie
ELEVEN_LABS_API_KEY=your_eleven_labs_api_key    # Registrate en una cuenta de pago según tu uso
VOICE_ID=sTgnjW6Su298ryjA5cNd                   # selecciona la voz desde elevenlabs, por defecto voz Prex
GOOGLE_PLACES_API_KEY=your_google_places_api_key # Registrate para tener acceso a google maps, gratis con un uso pequeño.
OPENAI_API_KEY=your_openai_api_key              # Consigue tu KEY en openai
TIMEZONEDB_API_KEY=your_timezonedb_api_key      # Consigue tu KEU en timezonedb, es gratis

Opcionales pero muy recomendables:
API TESSIE, link referido: https://share.tessie.com/nDAlwNM5LKb - IMPRESCINDIBLE para integración con el coche.
TIMEZONEDB - Para ver la hora local, útil si viajas y hay cambios horarios, la api key se puede conseguir gratis.
Google Places API - Si se le da poco uso puedes registrate grátis.

REQUISITOS OPERATIVOS:
Python 3.8+
Flask
openai
requests
python-dotenv
