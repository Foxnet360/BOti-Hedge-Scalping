# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Credenciales de Binance
API_KEY = os.getenv('BINANCE_API_KEY', '')
API_SECRET = os.getenv('BINANCE_API_SECRET', '')

# Verificar que las credenciales estén configuradas
if not API_KEY or not API_SECRET:
    raise ValueError("Las credenciales de Binance no están configuradas. "
                    "Por favor, configura BINANCE_API_KEY y BINANCE_API_SECRET "
                    "en el archivo .env o como variables de entorno.") 