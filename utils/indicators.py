# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

def calculate_rsi(prices, period=14):
    """
    Calcula el indicador RSI (Relative Strength Index)
    
    Args:
        prices: Serie de precios
        period: Período para el cálculo del RSI
        
    Returns:
        pandas.Series: Valores del RSI
    """
    # Convertir a numpy array si es necesario
    if isinstance(prices, pd.Series):
        prices = prices.values
    
    # Calcular cambios
    deltas = np.diff(prices)
    seed = deltas[:period+1]
    
    # Calcular ganancias y pérdidas
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    
    if down == 0:
        rs = float('inf')
    else:
        rs = up / down
    
    rsi = np.zeros_like(prices)
    rsi[:period] = 100. - 100. / (1. + rs)
    
    # Calcular RSI para el resto de los datos
    for i in range(period, len(prices)):
        delta = deltas[i-1]
        
        if delta > 0:
            upval = delta
            downval = 0
        else:
            upval = 0
            downval = -delta
        
        up = (up * (period - 1) + upval) / period
        down = (down * (period - 1) + downval) / period
        
        if down == 0:
            rs = float('inf')
        else:
            rs = up / down
        
        rsi[i] = 100. - 100. / (1. + rs)
    
    return pd.Series(rsi)

def calculate_macd(prices, fast_period=12, slow_period=26, signal_period=9):
    """
    Calcula el indicador MACD (Moving Average Convergence Divergence)
    
    Args:
        prices: Serie de precios
        fast_period: Período para la media móvil rápida
        slow_period: Período para la media móvil lenta
        signal_period: Período para la línea de señal
        
    Returns:
        tuple: (MACD, Signal, Histogram)
    """
    # Convertir a pandas Series si es necesario
    if not isinstance(prices, pd.Series):
        prices = pd.Series(prices)
    
    # Calcular EMAs
    ema_fast = prices.ewm(span=fast_period, adjust=False).mean()
    ema_slow = prices.ewm(span=slow_period, adjust=False).mean()
    
    # Calcular MACD
    macd = ema_fast - ema_slow
    
    # Calcular línea de señal
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    
    # Calcular histograma
    histogram = macd - signal
    
    return macd, signal, histogram

def calculate_bollinger_bands(prices, period=20, num_std=2):
    """
    Calcula las Bandas de Bollinger
    
    Args:
        prices: Serie de precios
        period: Período para la media móvil
        num_std: Número de desviaciones estándar
        
    Returns:
        tuple: (Upper Band, Middle Band, Lower Band)
    """
    # Convertir a pandas Series si es necesario
    if not isinstance(prices, pd.Series):
        prices = pd.Series(prices)
    
    # Calcular media móvil (banda media)
    middle_band = prices.rolling(window=period).mean()
    
    # Calcular desviación estándar
    std_dev = prices.rolling(window=period).std()
    
    # Calcular bandas superior e inferior
    upper_band = middle_band + (std_dev * num_std)
    lower_band = middle_band - (std_dev * num_std)
    
    return upper_band, middle_band, lower_band

def calculate_atr(high, low, close, period=14):
    """
    Calcula el ATR (Average True Range)
    
    Args:
        high: Serie de precios máximos
        low: Serie de precios mínimos
        close: Serie de precios de cierre
        period: Período para el cálculo
        
    Returns:
        pandas.Series: Valores del ATR
    """
    # Convertir a pandas Series si es necesario
    if not isinstance(high, pd.Series):
        high = pd.Series(high)
    if not isinstance(low, pd.Series):
        low = pd.Series(low)
    if not isinstance(close, pd.Series):
        close = pd.Series(close)
    
    # Calcular True Range
    prev_close = close.shift(1)
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # Calcular ATR
    atr = tr.rolling(window=period).mean()
    
    return atr
