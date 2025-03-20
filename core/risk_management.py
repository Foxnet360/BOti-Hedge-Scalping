# -*- coding: utf-8 -*-

import logging

class RiskManager:
    """Gestiona el riesgo de las operaciones"""
    
    def __init__(self, client, max_position_size=0.1, stop_loss_percent=0.02, take_profit_percent=0.04):
        """
        Inicializa el gestor de riesgos
        
        Args:
            client: Cliente de Binance
            max_position_size: Tamaño máximo de posición como porcentaje del balance (0.1 = 10%)
            stop_loss_percent: Porcentaje de stop loss (0.02 = 2%)
            take_profit_percent: Porcentaje de take profit (0.04 = 4%)
        """
        self.client = client
        self.max_position_size = max_position_size
        self.stop_loss_percent = stop_loss_percent
        self.take_profit_percent = take_profit_percent
        self.logger = logging.getLogger(__name__)
    
    def calculate_position_size(self, symbol, asset='USDT'):
        """
        Calcula el tamaño de posición basado en el balance disponible y el riesgo máximo
        
        Returns:
            float: Cantidad a comprar/vender
        """
        try:
            # Obtener balance disponible
            balance = self.client.get_account_balance(asset)
            
            # Obtener precio actual
            price = self.client.get_market_price(symbol)
            
            if not balance or not price:
                return 0
            
            # Calcular tamaño de posición
            position_value = balance * self.max_position_size
            position_size = position_value / price
            
            # Redondear a la precisión adecuada
            # Esto debería ajustarse según el símbolo
            position_size = round(position_size, 3)
            
            self.logger.info(f"Tamaño de posición calculado: {position_size} {symbol}")
            return position_size
        except Exception as e:
            self.logger.error(f"Error al calcular tamaño de posición: {e}")
            return 0
    
    def set_stop_loss(self, symbol, entry_price, side):
        """
        Establece un stop loss para la posición
        
        Args:
            symbol: Símbolo de trading
            entry_price: Precio de entrada
            side: 'BUY' o 'SELL'
        """
        try:
            if side == 'BUY':
                stop_price = entry_price * (1 - self.stop_loss_percent)
                order_side = 'SELL'
            else:
                stop_price = entry_price * (1 + self.stop_loss_percent)
                order_side = 'BUY'
            
            # Obtener posición actual
            position = self.client.get_position(symbol)
            if not position or position['amount'] == 0:
                return
            
            # Colocar orden de stop loss
            self.client.place_order(
                symbol=symbol,
                side=order_side,
                quantity=abs(position['amount']),
                order_type='STOP_MARKET',
                price=stop_price,
                reduce_only=True
            )
            
            self.logger.info(f"Stop loss establecido a {stop_price} para {symbol}")
        except Exception as e:
            self.logger.error(f"Error al establecer stop loss: {e}")
    
    def set_take_profit(self, symbol, entry_price, side):
        """
        Establece un take profit para la posición
        
        Args:
            symbol: Símbolo de trading
            entry_price: Precio de entrada
            side: 'BUY' o 'SELL'
        """
        try:
            if side == 'BUY':
                take_profit_price = entry_price * (1 + self.take_profit_percent)
                order_side = 'SELL'
            else:
                take_profit_price = entry_price * (1 - self.take_profit_percent)
                order_side = 'BUY'
            
            # Obtener posición actual
            position = self.client.get_position(symbol)
            if not position or position['amount'] == 0:
                return
            
            # Colocar orden de take profit
            self.client.place_order(
                symbol=symbol,
                side=order_side,
                quantity=abs(position['amount']),
                order_type='TAKE_PROFIT_MARKET',
                price=take_profit_price,
                reduce_only=True
            )
            
            self.logger.info(f"Take profit establecido a {take_profit_price} para {symbol}")
        except Exception as e:
            self.logger.error(f"Error al establecer take profit: {e}") 