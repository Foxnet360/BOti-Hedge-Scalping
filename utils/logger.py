# -*- coding: utf-8 -*-

import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(log_file='logs/trading_bot.log'):
    """Configura y devuelve un logger"""
    
    # Crear directorio de logs si no existe
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Configurar logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Formato de log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Handler para archivo con rotación
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10*1024*1024, backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Agregar handlers al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 