# Importar la lista de comandos y configuración del modelo
import pdb
from app.prex_config import *
from .debug import logger
# Función para detectar si la entrada es un comando válido


def detect_command(question):
    #    pdb.set_trace()  # debug
    logger.info('debug de comand detection')
    try:
        # Solicitud al modelo GPT para que detecte si el texto es un comando válido
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": f"{
                    commands_list}\nDetecta si el siguiente mensaje es un comando o sinónimos del comando, o que hagan referencia al mismo y cuál es el comando. Si no es un comando, responde 'No es un comando'."},
                {"role": "user", "content": question}
            ]
        )
        # Registrar el comando detectado en los logs
        logger.info('Command detected: %s',
                    completion.choices[0].message.content.strip())

        return completion.choices[0].message.content.strip()
        # return completion.choices[0].message['content'].strip()
    except Exception as e:
        # Manejo de errores en caso de fallo en la detección de comandos
        logger.info('error al detectar comando')
        return f"Error al detectar comando: {str(e)}"
