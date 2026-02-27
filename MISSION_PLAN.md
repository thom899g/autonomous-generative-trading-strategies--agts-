# Autonomous Generative Trading Strategies (AGTS)

## Objective
AGTS is a self-evolving AI system that generates novel trading strategies using generative models and optimizes them through reinforcement learning in simulated environments. The AI autonomously researches market patterns, creates innovative strategies, and refines them for optimal performance.

## Strategy
Research and implement using available tools.

## Execution Output
**SUMMARY**: I've created the foundational architecture for the Autonomous Generative Trading Strategies (AGTS) system with a modular, production-ready design. This includes core components for data management, strategy generation, backtesting, and RL optimization, all integrated with Firebase for state management and rigorous logging/error handling.

**OUTPUT**:

### FILE: requirements.txt
```
# Core Data & Computation
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
scipy>=1.11.0

# Time Series Analysis
statsmodels>=0.14.0

# Market Data
ccxt>=4.0.0
yfinance>=0.2.0
alpaca-trade-api>=3.0.0

# Machine Learning
tensorflow>=2.13.0
torch>=2.0.0

# Firebase Integration
firebase-admin>=6.2.0

# Utilities
python-dotenv>=1.0.0
loguru>=0.7.0
joblib>=1.3.0
tqdm>=4.65.0
```

### FILE: config/__init__.py
```python
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
```

### FILE: core/data_manager.py
```python
"""
Data Manager Module
Handles market data fetching, preprocessing, and storage with robust error handling.
Architectural Choice: Factory pattern for multiple data sources with common interface.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from dataclasses import dataclass
import ccxt
import yfinance as yf
import alpaca