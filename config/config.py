# -*- coding: utf-8 -*-

import os
import json
import logging

class Config:
    def __init__(self):
        # Parámetros por defecto
        self.CHECK_INTERVAL = 60  # segundos
        
        # Parámetros de estrategia Moving Average
        self.MA_SHORT_WINDOW = 9
        self.MA_LONG_WINDOW = 21
        
        # Parámetros de estrategia RSI
        self.RSI_PERIOD = 14
        self.RSI_OVERBOUGHT = 70
        self.RSI_OVERSOLD = 30
        
        # Gestión de riesgos
        self.MAX_POSITION_SIZE = 0.1  # 10% del balance disponible
        self.STOP_LOSS_PERCENT = 0.02  # 2% de stop loss
        self.TAKE_PROFIT_PERCENT = 0.04  # 4% de take profit
        
        # Configuración de trading
        self.LEVERAGE = 2  # Apalancamiento
        self.ORDER_TYPE = 'MARKET'  # Tipo de orden: MARKET o LIMIT
        
    def load_config(self, config_file='config/settings.json'):
        """Carga la configuración desde un archivo JSON"""
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config_data = json.load(f)
                
                # Actualizar atributos desde el archivo
                for key, value in config_data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
                
                logging.info(f"Configuración cargada desde {config_file}")
            except Exception as e:
                logging.error(f"Error al cargar la configuración: {e}")
        else:
            logging.warning(f"Archivo de configuración {config_file} no encontrado. Usando valores por defecto.")
            
    def save_config(self, config_file='config/settings.json'):
        """Guarda la configuración actual en un archivo JSON"""
        config_data = {attr: getattr(self, attr) for attr in dir(self) 
                      if not attr.startswith('__') and not callable(getattr(self, attr))}
        
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        
        try:
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=4)
            logging.info(f"Configuración guardada en {config_file}")
        except Exception as e:
            logging.error(f"Error al guardar la configuración: {e}") 