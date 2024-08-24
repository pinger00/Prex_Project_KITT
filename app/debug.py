import logging

# Configurar el logging básico
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Crear un logger
logger = logging.getLogger(__name__)
