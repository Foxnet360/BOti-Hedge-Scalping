#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import argparse
from config.config import Config
from core.exchange import BinanceClient
from strategies.moving_average import MovingAverageStrategy
from strategies.rsi_strategy import RSIStrategy
from utils.logger import setup_logger

logger = setup_logger()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Binance Futures Trading Bot')
    parser.add_argument('--strategy', type=str, default='ma', choices=['ma', 'rsi'],
                        help='Trading strategy to use (ma: Moving Average, rsi: RSI)')
    parser.add_argument('--symbol', type=str, default='BTCUSDT',
                        help='Trading pair symbol (e.g., BTCUSDT, ETHUSDC)')
    parser.add_argument('--interval', type=str, default='1h',
                        help='Candlestick interval (e.g., 1m, 5m, 15m, 1h, 4h, 1d)')
    parser.add_argument('--test', action='store_true',
                        help='Run in test mode (no real trades)')
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Cargar configuración
    config = Config()
    config.load_config()
    
    # Inicializar cliente de Binance
    client = BinanceClient(test_mode=args.test)
    
    # Seleccionar estrategia
    if args.strategy == 'ma':
        strategy = MovingAverageStrategy(
            client=client,
            symbol=args.symbol,
            interval=args.interval,
            short_window=config.MA_SHORT_WINDOW,
            long_window=config.MA_LONG_WINDOW
        )
    elif args.strategy == 'rsi':
        strategy = RSIStrategy(
            client=client,
            symbol=args.symbol,
            interval=args.interval,
            rsi_period=config.RSI_PERIOD,
            rsi_overbought=config.RSI_OVERBOUGHT,
            rsi_oversold=config.RSI_OVERSOLD
        )
    
    logger.info(f"Iniciando bot con estrategia {args.strategy} para {args.symbol} en intervalo {args.interval}")
    
    try:
        while True:
            strategy.execute()
            time.sleep(config.CHECK_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Bot detenido manualmente")
    except Exception as e:
        logger.error(f"Error en la ejecución del bot: {e}")
    finally:
        logger.info("Cerrando bot")

if __name__ == "__main__":
    main() 