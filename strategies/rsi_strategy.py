# -*- coding: utf-8 -*-

import pandas as pd
from core.strategy import Strategy
from core.risk_management import RiskManager
from utils.indicators import calculate_rsi

class RSIStrategy(Strategy):
    """Estrategia basada en el indicador RSI (Relative Strength Index)"""
    
    def __init__(self, client, symbol, interval, rsi_period=14, rsi_overbought=70, rsi_oversold=30):
        super().__init__(client, symbol, interval)
        self.rsi_period = rsi_period
        self.rsi_overbought = rsi_overbought
        self.rsi_oversold = rsi_oversold
        self.risk_manager = RiskManager(client)
    
    def analyze(self):
        """
        Analiza el mercado usando el indicador RSI
        
        Returns:
            str: 'BUY', 'SELL' o None
        """
        # Obtener datos históricos
        klines = self.client.get_historical_klines(
            symbol=self.symbol,
            interval=self.interval,
            limit=self.rsi_period + 10  # Obtener suficientes datos
        )
        
        if not klines or len(klines) < self.rsi_period + 2:
            self.logger.warning(f"Datos insuficientes para {self.symbol}")
            return None
        
        # Convertir a DataFrame
        df = pd.DataFrame(klines)
        
        # Calcular RSI
        df['rsi'] = calculate_rsi(df['close'], self.rsi_period)
        
        # Eliminar filas con NaN
        df = df.dropna()
        
        if len(df) < 2:
            return None
        
        # Obtener valores actuales y anteriores de RSI
        current_rsi = df['rsi'].iloc[-1]
        previous_rsi = df['rsi'].iloc[-2]
        
        # Señal de compra: RSI cruza por encima del nivel de sobreventa
        if previous_rsi < self.rsi_oversold and current_rsi >= self.rsi_oversold:
            return 'BUY'
        
        # Señal de venta: RSI cruza por debajo del nivel de sobrecompra
        elif previous_rsi > self.rsi_overbought and current_rsi <= self.rsi_overbought:
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