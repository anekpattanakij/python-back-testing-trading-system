from robot.base.robo_base import RoboTrade
from robot.base.robo_indicator import calculate_ema
from robot.base.robo_enum import PriceDataDictColumn, CommandType, OrderType, OrderSide
import math


class Ema12Cross50Robo(RoboTrade):

    def action1d(self):
        self.data1d = calculate_ema(
            self.data1d, PriceDataDictColumn.CLOSE, "ema_12", 12)
        self.data1d = calculate_ema(
            self.data1d, PriceDataDictColumn.CLOSE, "ema_26", 26)
        if math.isnan(self.data1d[0]["ema_12"]) or math.isnan(self.data1d[0]["ema_26"]):
            return []

        command_list = []
        if self.data1d[0]["ema_12"] >= self.data1d[0]["ema_26"] and self.data1d[1]["ema_12"] < self.data1d[1]["ema_26"] and self.data1d[0][PriceDataDictColumn.CLOSE] > self.data1d[0]["ema_12"]:
            command_list.append({"type": CommandType.ALERT, "message": "EMA 12 Cross over EMAR 26 in 1d at price {0}".format(
                self.data4h[0][PriceDataDictColumn.CLOSE])})
            if len(self.position_list) == 0:
                command_list.append({
                    "type": CommandType.ORDER,
                    "order": OrderType.LIMIT,
                    "side": OrderSide.LONG,
                    "qty": self.fund/self.data1d[0][PriceDataDictColumn.CLOSE],
                    "price": self.data1d[0][PriceDataDictColumn.CLOSE]
                })

        if self.data1d[0]["ema_12"] < self.data1d[0]["ema_26"] and self.data1d[1]["ema_12"] >= self.data1d[1]["ema_26"]:
            command_list.append({"type": CommandType.ALERT, "message": "EMA 12 Cross under EMAR 26 in 1d at price {0}".format(
                self.data4h[0][PriceDataDictColumn.CLOSE])})
            if len(self.position_list) > 0:
                command_list.append({
                    "type": CommandType.ORDER,
                    "order": OrderType.LIMIT,
                    "side": OrderSide.SHORT,
                    "qty": self.position_list[0]["qty"],
                    "price": self.data1d[0][PriceDataDictColumn.CLOSE]
                })

        return command_list
