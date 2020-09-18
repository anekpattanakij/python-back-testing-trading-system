from enum import Enum

class CommandType(Enum):
    ALERT = 'ALERT'
    ORDER = 'ORDER'
    CANCEL = 'CANCEL'
    CANCEL_ALL = 'CANCEL_ALL'

class OrderSide(Enum):
    LONG = 1
    SHORT = -1

class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP_LIMIT = "STOP_LIMIT" 
    STOP_MARKET = "STOP_MARKET"  
    TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT" 
    TAKE_PROFIT_MARKET = "TAKE_PROFIT_MARKET"  
    TRALING_STOP = "TRALING_STOP" 

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
