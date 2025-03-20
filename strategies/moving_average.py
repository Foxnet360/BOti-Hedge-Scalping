# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from core.strategy import Strategy
from core.risk_management import RiskManager

class MovingAverageStrategy(Strategy):
    """Estrategia basada en cruce de medias móviles"""
    
    def __init__(self, client, symbol, interval, short_window=9, long_window=21):
        super().__init__(client, symbol, interval)
        self.short_window = short_window
        self.long_window = long_window
        self.risk_manager = RiskManager(client)
    
    def analyze(self):
        """
        Analiza el mercado usando cruce de medias móviles
        
        Returns:
            str: 'BUY', 'SELL' o None
        """
        # Obtener datos históricos
        klines = self.client.get_historical_klines(
            symbol=self.symbol,
            interval=self.interval,
            limit=self.long_window + 10  # Obtener suficientes datos
        )
        
        if not klines or len(klines) < self.long_window:
            self.logger.warning(f"Datos insuficientes para {self.symbol}")
            return None
        
        # Convertir a DataFrame
        df = pd.DataFrame(klines)
        
        # Calcular medias móviles
        df['ma_short'] = df['close'].rolling(window=self.short_window).mean()
        df['ma_long'] = df['close'].rolling(window=self.long_window).mean()
        
        # Eliminar filas con NaN
        df = df.dropna()
        
        if len(df) < 2:
            return None
        
        # Verificar cruce de medias móviles
        current = df.iloc[-1]
        previous = df.iloc[-2]
        
        # Cruce alcista: MA corta cruza por encima de MA larga
        if (previous['ma_short'] <= previous['ma_long']) and (current['ma_short'] > current['ma_long']):
            return 'BUY'
        
        # Cruce bajista: MA corta cruza por debajo de MA larga
        elif (previous['ma_short'] >= previous['ma_long']) and (current['ma_short'] < current['ma_long']):
            return 'SELL'
        
        return None
    
    def calculate_position_size(self, signal):
        """
        Calcula el tamaño de la posición basado en la gestión de riesgos
        
        Args:
            signal: 'BUY' o 'SELL'
            
        Returns:
            float: Cantidad a comprar/vender
        """
        return self.risk_manager.calculate_position_size(self.symbol) 