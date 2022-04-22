from decimal import Decimal
market_price_range = {"UP": 1.3, "DOWN": 0.7}
min_order_amount = {"BTCUSDT": Decimal(0.000001), "ETHUSDT": Decimal(
    0.00001), "BNBUSDT": Decimal(0.0001)}
min_order_usdt = {"BTCUSDT": Decimal(
    10), "ETHUSDT": Decimal(10), "BNBUSDT": Decimal(10)}
order_spread_usdt = {"BTCUSDT": Decimal(
    0.01), "ETHUSDT": Decimal(0.01), "BNBUSDT": Decimal(0.01)}
