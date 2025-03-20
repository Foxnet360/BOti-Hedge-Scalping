# -*- coding: utf-8 -*-

import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
from config.credentials import API_KEY, API_SECRET

class BinanceClient:
    def __init__(self, test_mode=False):
        self.client = Client(API_KEY, API_SECRET)
        self.test_mode = test_mode
        self.logger = logging.getLogger(__name__)
        
        # Verificar conexión
        try:
            self.client.ping()
            self.logger.info("Conexión con Binance establecida correctamente")
        except BinanceAPIException as e:
            self.logger.error(f"Error al conectar con Binance: {e}")
            raise
    
    def get_account_balance(self, asset='USDT'):
        """Obtiene el balance de una moneda específica"""
        try:
            futures_account = self.client.futures_account()
            for balance in futures_account['assets']:
                if balance['asset'] == asset:
                    return float(balance['availableBalance'])
            return 0.0
        except BinanceAPIException as e:
            self.logger.error(f"Error al obtener balance: {e}")
            return 0.0
    
    def get_market_price(self, symbol):
        """Obtiene el precio actual de un símbolo"""
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except BinanceAPIException as e:
            self.logger.error(f"Error al obtener precio de mercado: {e}")
            return None
    
    def get_historical_klines(self, symbol, interval, limit=100):
        """Obtiene velas históricas para un símbolo e intervalo"""
        try:
            klines = self.client.futures_klines(symbol=symbol, interval=interval, limit=limit)
            return [
                {
                    'timestamp': k[0],
                    'open': float(k[1]),
                    'high': float(k[2]),
                    'low': float(k[3]),
                    'close': float(k[4]),
                    'volume': float(k[5])
                }
                for k in klines
            ]
        except BinanceAPIException as e:
            self.logger.error(f"Error al obtener datos históricos: {e}")
            return []
    
    def place_order(self, symbol, side, quantity, order_type='MARKET', price=None, reduce_only=False):
        """Coloca una orden en el mercado de futuros"""
        if self.test_mode:
            self.logger.info(f"[TEST MODE] Orden: {side} {quantity} {symbol} a {price if price else 'precio de mercado'}")
            return {"orderId": "test", "status": "TEST"}
        
        try:
            params = {
                'symbol': symbol,
                'side': side,  # 'BUY' o 'SELL'
                'quantity': quantity,
                'reduceOnly': reduce_only
            }
            
            if order_type == 'LIMIT' and price:
                params['type'] = 'LIMIT'
                params['price'] = price
                params['timeInForce'] = 'GTC'
            else:
                params['type'] = 'MARKET'
            
            order = self.client.futures_create_order(**params)
            self.logger.info(f"Orden colocada: {side} {quantity} {symbol}")
            return order
        except BinanceAPIException as e:
            self.logger.error(f"Error al colocar orden: {e}")
            return None
    
    def set_leverage(self, symbol, leverage):
        """Configura el apalancamiento para un símbolo"""
        try:
            response = self.client.futures_change_leverage(symbol=symbol, leverage=leverage)
            self.logger.info(f"Apalancamiento configurado a {leverage}x para {symbol}")
            return response
        except BinanceAPIException as e:
            self.logger.error(f"Error al configurar apalancamiento: {e}")
            return None
    
    def get_position(self, symbol):
        """Obtiene la posición actual para un símbolo"""
        try:
            positions = self.client.futures_position_information(symbol=symbol)
            if positions:
                position = positions[0]
                return {
                    'symbol': position['symbol'],
                    'amount': float(position['positionAmt']),
                    'entry_price': float(position['entryPrice']),
                    'unrealized_pnl': float(position['unRealizedProfit']),
                    'leverage': int(position['leverage'])
                }
            return None
        except BinanceAPIException as e:
            self.logger.error(f"Error al obtener posición: {e}")
            return None 