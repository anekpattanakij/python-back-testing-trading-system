
class RoboTrade:
    '''
      pricelist will be in array of dictionary with 200 lenght
      newest time slot will be store in index [0]
      oldest time slot will be store in index [199]
      {
        "opentime" : 155552000, # in milli-second format
        "open" : 110.0,
        "close" : 100.0,
        "high" : 120.0,
        "low" : 90.0,
        "highlow" : 30.0, # high - low
        "highopen" : 20.0, # high - open
        "closelow" : 10.0, # close - low
        "closeopen" : -10.0, # close - open
        "ohlc4" : 105.0
      }
    '''
    data5m = []
    data15m = []
    data30m = []
    data1h = []
    data2h = []
    data4h = []
    data1d = []
    data1w = []
    '''
  position_list is using for trading and back testing strategy, it will be array of current position holding
   {
      "order_id" : 12345,
      "create_time" : 12321213, # time in milli second
      "price" : 9000.0,
      "side" : OrderSide,
      "status": OrderStatus,
      "qty" : 1.0, # float / mandatory for LIMIT / will be ignore for MARKET
      "filled" : 0.7 # it can be partial match
      "sold" : 0.2 # it can be partial sell
    }
  '''
    fund = 0.0
    position_list = []
    '''
    each action should return array of command
    command can be 2 dict type

    alert
    {
      "type" : CommandType.ALERT,
      "message" : ""
    }

    order
    {
      "type" : CommandType.ORDER,
      "order" : OrderType.ENUM,
      "side" : OrderSide,
      "qty" : 1.0, # float
      "price" : 9871.12 # float / mandatory for LIMIT / will be ignore for MARKET
    }
  '''

    def __init__(self):
        pass

    def action5m(self):
        pass

    def action15m(self):
        pass

    def action30m(self):
        pass

    def action1h(self):
        pass

    def action2h(self):
        pass

    def action4h(self):
        pass

    def action1d(self):
        pass

 
    def action1w(self):
      pass

    # return total value sum with filled position value
    def total_port_value(self):
        return self.fund + sum(position['price'] * (position['filled'] - position['sold']) for position in self.position_list)
    # return total value sum with filled position value and deduct open position to limit trade side
    def total_port_trade_value(self):
        return self.fund + sum(position['price'] * (position['filled'] - position['sold']) for position in self.position_list) - sum(position['price'] * (position['qty'] - position['filled'] - position['sold']) for position in self.position_list)
    # return total value sum with filled position value and deduct open position to limit trade side
    def total_open_position_qty(self):
        return self.fund + sum(position['qty'] - position['sold'] for position in self.position_list) 
