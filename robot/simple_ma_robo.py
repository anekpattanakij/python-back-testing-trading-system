from robot.base.robo_base import RoboTrade
from robot.base.robo_indicator import calculate_ma
from robot.base.robo_enum import PriceDataDictColumn, CommandType, OrderType, OrderSide
import math


class SimpleMaRobo(RoboTrade):

    def action2h(self):
        self.data2h = calculate_ma(self.data2h, PriceDataDictColumn.CLOSE, "ma_12", 12)
        self.data2h = calculate_ma(self.data2h, PriceDataDictColumn.CLOSE, "ma_26", 26)
        if math.isnan(self.data2h[0]["ma_12"]) or  math.isnan(self.data2h[0]["ma_26"]) :
            return []

        order_qty = self.fund / self.data2h[0][PriceDataDictColumn.CLOSE]
        if len(self.position_list) == 0 and self.data2h[0]["ma_12"] > self.data2h[0]["ma_26"] :
            return [{
                "type": CommandType.ORDER,
                "order": OrderType.LIMIT,
                "side": OrderSide.LONG,
                "qty": order_qty,
                "price": self.data2h[0][PriceDataDictColumn.CLOSE]
            }]

        if len(self.position_list) > 0 and self.data2h[0]["ma_12"] < self.data2h[0]["ma_26"]:
            return [{
                "type": CommandType.CLOSE_ALL
            }]

        return []
