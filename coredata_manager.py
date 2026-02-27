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