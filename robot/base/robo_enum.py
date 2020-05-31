from enum import Enum

class CommandType(Enum):
    ALERT = 'ALERT'
    ORDER = 'ORDER'

class OrderSide(Enum):
    LONG = 1
    SHORT = -1

class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    EXIT = "EXIT" # exit last strategy with market price
    EXIT_ALL = "EXIT_ALL"  # exit all strategy with market price

class OrderStatus(Enum):
    OPEN = "OPEN"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"

class PriceDataDictColumn(Enum):
    OPENTIME = "opentime"
    OPEN = "open"
    CLOSE = "close"
    HIGH = "high"
    LOW = "low"
    HIGHLOW = "highlow"
    HIGHOPEN = "highopen"
    CLOSELOW = "closelow"
    CLOSEOPEN = "closeopen"
    OHLC4 = "ohlc4"
