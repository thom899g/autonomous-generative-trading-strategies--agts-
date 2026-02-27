"""
Configuration module for AGTS system.
Centralizes all configuration parameters with environment-aware defaults.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class DatabaseConfig:
    """Firebase configuration"""
    firebase_credentials_path: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase_credentials.json")
    firestore_collection: str = os.getenv("FIRESTORE_COLLECTION", "agts_strategies")
    realtime_db_url: Optional[str] = os.getenv("FIREBASE_REALTIME_DB_URL")

@dataclass
class DataConfig:
    """Data fetching and preprocessing configuration"""
    default_timeframe: str = "1h"
    lookback_periods: int = 5000
    train_test_split: float = 0.8
    validation_split: float = 0.1
    symbols: tuple = ("BTC/USDT", "ETH/USDT", "AAPL", "MSFT")
    data_sources: tuple = ("ccxt", "yfinance", "alpaca")

@dataclass
class StrategyConfig:
    """Strategy generation configuration"""
    max_indicators_per_strategy: int = 5
    max_rules_per_strategy: int = 10
    min_confidence_threshold: float = 0.7
    population_size: int = 100
    elite_size: int = 10

@dataclass
class BacktestConfig:
    """Backtesting configuration"""
    initial_capital: float = 100000.0
    commission: float = 0.001  # 0.1%
    slippage: float = 0.0005   # 0.05%
    risk_free_rate: float = 0.02
    max_drawdown_limit: float = 0.2  # 20%

@dataclass
class RLConfig:
    """Reinforcement learning configuration"""
    learning_rate: float = 0.001
    discount_factor: float = 0.99
    batch_size: int = 32
    memory_size: int = 10000
    exploration_rate: float = 0.3
    exploration_decay: float = 0.995

@dataclass
class LoggingConfig:
    """Logging configuration"""
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = "agts_system.log"
    max_file_size: str = "10MB"
    backup_count: int = 5

@dataclass
class AGTSConfig:
    """Master configuration container"""
    database: DatabaseConfig = DatabaseConfig()
    data: DataConfig = DataConfig()
    strategy: StrategyConfig = StrategyConfig()
    backtest: BacktestConfig = BacktestConfig()
    rl: RLConfig = RLConfig()
    logging: LoggingConfig = LoggingConfig()

# Global configuration instance
config = AGTSConfig()