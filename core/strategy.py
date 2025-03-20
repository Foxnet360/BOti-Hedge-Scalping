# -*- coding: utf-8 -*-

import logging
from abc import ABC, abstractmethod

class Strategy(ABC):
    """Clase base abstracta para todas las estrategias de trading"""
    
    def __init__(self, client, symbol, interval):
        self.client = client
        self.symbol = symbol
        self.interval = interval
        self.logger = logging.getLogger(__name__)
    
    @abstractmethod
    def analyze(self):
        """
        Analiza el mercado y determina la señal de trading
        Debe devolver: 'BUY', 'SELL' o None
        """
        pass
    
    @abstractmethod
    def calculate_position_size(self, signal):
        """
        Calcula el tamaño de la posición basado en la señal y la gestión de riesgos
        """
        pass
    
    def execute(self):
        """Ejecuta la estrategia: analiza el mercado y opera si hay señal"""
        signal = self.analyze()
        
        if not signal:
            self.logger.info(f"No hay señal para {self.symbol}")
            return
        
        # Obtener posición actual
        position = self.client.get_position(self.symbol)
        position_amount = position['amount'] if position else 0
        
        # Determinar acción basada en la señal y posición actual
        if signal == 'BUY' and position_amount <= 0:
            # Si la señal es comprar y no tenemos posición larga
            quantity = self.calculate_position_size(signal)
            
            # Si tenemos posición corta, primero cerrarla
            if position_amount < 0:
                self.client.place_order(
                    symbol=self.symbol,
                    side='BUY',
                    quantity=abs(position_amount),
                    reduce_only=True
                )
                self.logger.info(f"Posición corta cerrada para {self.symbol}")
            
            # Abrir posición larga
            if quantity > 0:
                self.client.place_order(
                    symbol=self.symbol,
                    side='BUY',
                    quantity=quantity
                )
                self.logger.info(f"Posición larga abierta: {quantity} {self.symbol}")
                
        elif signal == 'SELL' and position_amount >= 0:
            # Si la señal es vender y no tenemos posición corta
            quantity = self.calculate_position_size(signal)
            
            # Si tenemos posición larga, primero cerrarla
            if position_amount > 0:
                self.client.place_order(
                    symbol=self.symbol,
                    side='SELL',
                    quantity=position_amount,
                    reduce_only=True
                )
                self.logger.info(f"Posición larga cerrada para {self.symbol}")
            
            # Abrir posición corta
            if quantity > 0:
                self.client.place_order(
                    symbol=self.symbol,
                    side='SELL',
                    quantity=quantity
                )
                self.logger.info(f"Posición corta abierta: {quantity} {self.symbol}") 