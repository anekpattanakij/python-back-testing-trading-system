import sys
import inspect
import pkgutil
import math
from timeit import default_timer as timer
import pandas as pd
import numpy as np
from pathlib import Path
from importlib import import_module
from decimal import Decimal
import decimal
from robot.base.robo_base import RoboTrade
from robot.base.robo_enum import OrderType, PriceDataDictColumn, CommandType, OrderSide, OrderStatus
from common_function import find_column_number, add_close_open, add_high_low, add_high_open, add_close_low, add_ohlc4
from config import min_order_amount, min_order_usdt, order_spread_usdt

# configuration
TEST_DATA_2018_CURRENT = './test_data/btc_usdt_test_data.csv'
TARGET_ROBOT = 'robo'
LIMIT_HISTORY_PRICE = 200
INITIAL_FUND = Decimal(10000.0)
COMMISION_FEE = Decimal(0.1)
FILL_ORDER_AT_CLOSE_PRICE = True
CURRENT_SYMBOL = 'BTCUSDT'

# constant
ROBOT_BASE_CLASS = 'RoboTrade'
MULTIPLY_15M = 3
MULTIPLY_30M = 6
MULTIPLY_1H = 12
MULTIPLY_2H = 24
MULTIPLY_4H = 48
MULTIPLY_1D = 288
MULTIPLY_1W = 2016


def convert_price_to_dictionary(input_object, header_position):
    return {
        # in milli-second format
        PriceDataDictColumn.OPENTIME: input_object[header_position['opentime']],
        PriceDataDictColumn.OPEN: Decimal(input_object[header_position['open']]),
        PriceDataDictColumn.CLOSE: Decimal(input_object[header_position['close']]),
        PriceDataDictColumn.HIGH: Decimal(input_object[header_position['high']]),
        PriceDataDictColumn.LOW: Decimal(input_object[header_position['low']]),
        # high - low
        PriceDataDictColumn.HIGHLOW: Decimal(input_object[header_position['highlow']]),
        # high - open
        PriceDataDictColumn.HIGHOPEN: Decimal(input_object[header_position['highopen']]),
        # close - low
        PriceDataDictColumn.CLOSELOW: Decimal(input_object[header_position['closelow']]),
        # close - open
        PriceDataDictColumn.CLOSEOPEN: Decimal(input_object[header_position['closeopen']]),
        PriceDataDictColumn.OHLC4: Decimal(
            input_object[header_position['ohlc4']])
    }


def merge_data_tf(list_df):
    # list_df : array of dictionary
    new_high, new_low = Decimal(0.0), Decimal(99999999.0)
    for i in range(len(list_df)):
        if(list_df[i][PriceDataDictColumn.LOW] < new_low):
            new_low = list_df[i][PriceDataDictColumn.LOW]
        if(list_df[i][PriceDataDictColumn.HIGH] > new_high):
            new_high = list_df[i][PriceDataDictColumn.HIGH]
    return {
        # in milli-second format
        PriceDataDictColumn.OPENTIME: list_df[-1][PriceDataDictColumn.OPENTIME],
        PriceDataDictColumn.OPEN: list_df[-1][PriceDataDictColumn.OPEN],
        PriceDataDictColumn.CLOSE: list_df[0][PriceDataDictColumn.CLOSE],
        PriceDataDictColumn.HIGH: new_high,
        PriceDataDictColumn.LOW: new_low,
        PriceDataDictColumn.HIGHLOW: new_high - new_low,  # high - low
        # high - open
        PriceDataDictColumn.HIGHOPEN: new_high - list_df[-1][PriceDataDictColumn.OPEN],
        # close - low
        PriceDataDictColumn.CLOSELOW: list_df[0][PriceDataDictColumn.CLOSE] - new_low,
        # close - open
        PriceDataDictColumn.CLOSEOPEN: list_df[0][PriceDataDictColumn.CLOSE] - list_df[-1][PriceDataDictColumn.OPEN],
        PriceDataDictColumn.OHLC4: (
            list_df[0][PriceDataDictColumn.CLOSE] + list_df[-1][PriceDataDictColumn.OPEN] + new_high + new_low)/4
    }


def cut_limit_history(list_df):
    if len(list_df) > LIMIT_HISTORY_PRICE:
        return list_df[:200]
    return list_df


def concat_list(source_list, add_list):
    if(type(add_list) == type([])):
        source_list = source_list + add_list
    else:
        try:
            if add_list['type'] == CommandType.ORDER or add_list['type'] == CommandType.ALERT:
                source_list = source_list + [add_list]
        except:
            pass
    return source_list


if __name__ == '__main__':
    target_robo = {}
    name = ''
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_DOWN
    ctx.prec = 8
    for (_, name, _) in pkgutil.iter_modules([Path('./robot')]):
        if not Path('./robot/' + name).is_dir():
            if name == TARGET_ROBOT:
                target_robo = import_module('robot.' + name, package=__name__)

    for i in dir(target_robo):
        attribute = getattr(target_robo, i)
        if inspect.isclass(attribute) and issubclass(attribute, RoboTrade) and attribute.__name__ != RoboTrade.__name__:
            setattr(sys.modules[__name__], name, attribute)
            target_robo_class = attribute

    start = timer()
    df = pd.read_csv(TEST_DATA_2018_CURRENT)
    df_np = df.to_numpy()
    df_header = list(df)
    df_np, df_header = add_close_open(df_np, df_header)
    df_np, df_header = add_high_low(df_np, df_header)
    df_np, df_header = add_high_open(df_np, df_header)
    df_np, df_header = add_close_low(df_np, df_header)
    df_np, df_header = add_ohlc4(df_np, df_header)
    header_position_list = {
        'opentime': find_column_number(df_header, 'open-time'),
        'open': find_column_number(df_header, 'open-price'),
        'close': find_column_number(df_header, 'close-price'),
        'high': find_column_number(df_header, 'high-price'),
        'low': find_column_number(df_header, 'low-price'),
        'highlow': find_column_number(df_header, 'high-low'),
        'highopen': find_column_number(df_header, 'high-open'),
        'closelow': find_column_number(df_header, 'close-low'),
        'closeopen': find_column_number(df_header, 'close-open'),
        'ohlc4': find_column_number(df_header, 'ohlc4')
    }

    '''
    dictionary in trade list 
    {
        pre_fund : 1222.0,
        last_fund  : 1555.0,
        buy_otder : {
            'order_id' : 1
            'time' : 112554555 # millisecond,
            'price' : 9500.0,
            'qty' : 1.0,
            'match' ' :0.5,
            'side' : OrderSide,
        },
        sell_otder : {
            'order_id' : 2
            'time' : 112554555 # millisecond,
            'price' : 9500.0,
            'qty' : 1.0,
            'match' ' :0.5,
            'side' : OrderSide,
        }
    }
    '''
    trade_history_list = []
    position_list = []
    target_robo = target_robo_class()
    data5m, data15m, data30m, data1h, data2h, data4h, data1d, data1w = [
    ], [], [], [], [], [], [], []
    target_robo.fund = INITIAL_FUND
    running_order_id = 1
    for i in range(len(df_np)):
        dict5m = [convert_price_to_dictionary(df_np[i], header_position_list)]
        # use current dict data to fill/close position before calculate new position
        for pos_index in range(len(target_robo.position_list)):
            if target_robo.position_list[pos_index]['status'] == OrderStatus.OPEN:
                if (target_robo.position_list[pos_index]['price'] <= dict5m[0][PriceDataDictColumn.HIGH]) and (target_robo.position_list[pos_index]['price'] >= dict5m[0][PriceDataDictColumn.LOW]):
                    # deduct fund
                    target_robo.position_list[pos_index]['status'] = OrderStatus.FILLED
        # settlement long short
        running_row = 0
        process_position_list = []
        while running_row < len(target_robo.position_list):
            if(target_robo.position_list[running_row]['status'] != OrderStatus.FILLED):
                running_row = running_row+1
            else:
                if len(process_position_list) == 0 or (process_position_list[0]['side'] == target_robo.position_list[running_row]['side']):
                    # same side as first, so no settlement
                    process_position_list.append(
                        target_robo.position_list[running_row])
                    running_row = running_row + 1
                else:
                    # different side from waiting settlement list, so settelment
                    value_settle = min(process_position_list[0]['qty']-process_position_list[0]['filled'],
                                       target_robo.position_list[running_row]['qty'] - target_robo.position_list[running_row]['filled'])
                    process_position_list[0]['filled'] = process_position_list[0]['filled'] + value_settle
                    target_robo.position_list[running_row]['filled'] = target_robo.position_list[running_row]['filled'] + value_settle

                    fund_before = target_robo.fund
                    # calculate settlement
                    target_robo.fund = target_robo.fund + (value_settle * process_position_list[0]['price'] * (-1 if process_position_list[0]['side'] == OrderSide.LONG else 1)) + (
                        value_settle * target_robo.position_list[running_row]['price'] * (-1 if target_robo.position_list[running_row]['side'] == OrderSide.LONG else 1))
                    # add trade to history
                    trade_history_list = trade_history_list + \
                        [{
                            'pre_fund': fund_before,
                            'last_fund': target_robo.fund,
                            'buy_order': {
                                'order_id': process_position_list[0]['order_id'],
                                'time': process_position_list[0]['create_time'],
                                'price':  process_position_list[0]['price'],
                                'qty':  process_position_list[0]['qty'],
                                'match': process_position_list[0]['filled'],
                                'side':  process_position_list[0]['side']
                            },
                            'sell_order': {
                                'order_id': target_robo.position_list[running_row]['order_id'],
                                'time': target_robo.position_list[running_row]['create_time'],
                                'price':  target_robo.position_list[running_row]['price'],
                                'qty':  target_robo.position_list[running_row]['qty'],
                                'match': target_robo.position_list[running_row]['filled'],
                                'side':  target_robo.position_list[running_row]['side']
                            }}]
                    print('trade : ', trade_history_list[-1])
                    # remove position if fill all
                    if target_robo.position_list[running_row]['filled'] == target_robo.position_list[running_row]['qty']:
                        target_robo.position_list = target_robo.position_list[
                            :running_row] + target_robo.position_list[running_row+1:]
                    if process_position_list[0]['filled'] == process_position_list[0]['qty']:
                        # remove original position in trading list
                        for running_index in range(running_row):
                            if target_robo.position_list[running_index]['order_id'] == process_position_list[0]['order_id'] and target_robo.position_list[running_index]['create_time'] == process_position_list[0]['create_time'] and target_robo.position_list[running_index]['qty'] == process_position_list[0]['qty']:
                                target_robo.position_list = target_robo.position_list[
                                    :running_index] + target_robo.position_list[running_index+1:]
                                running_row = running_row - 1
                                break
                        # remove from process trading list
                        process_position_list = process_position_list[1:]
        # run action
        data5m = dict5m + data5m
        target_robo.data5m = cut_limit_history(data5m)
        return_command_list = target_robo.action5m()
        command_list = []
        if (i+1) % MULTIPLY_15M == 0:
            data15m = [merge_data_tf(data5m[:MULTIPLY_15M])] + data15m
            target_robo.data15m = cut_limit_history(data15m)
            command_list = concat_list(command_list, target_robo.action15m())
        if (i+1) % MULTIPLY_30M == 0:
            data30m = [merge_data_tf(data5m[:MULTIPLY_30M])] + data30m
            target_robo.data30m = cut_limit_history(data30m)
            command_list = concat_list(command_list, target_robo.action30m())
        if (i+1) % MULTIPLY_1H == 0:
            data1h = [merge_data_tf(data5m[:MULTIPLY_1H])] + data1h
            target_robo.data1h = cut_limit_history(data1h)
            command_list = concat_list(command_list, target_robo.action1h())
        if (i+1) % MULTIPLY_2H == 0:
            data2h = [merge_data_tf(data5m[:MULTIPLY_2H])] + data2h
            target_robo.data2h = cut_limit_history(data2h)
            command_list = concat_list(command_list, target_robo.action2h())
        if (i+1) % MULTIPLY_4H == 0:
            data4h = [merge_data_tf(data5m[:MULTIPLY_4H])] + data4h
            target_robo.data4h = cut_limit_history(data4h)
            command_list = concat_list(command_list, target_robo.action4h())
        if (i+1) % MULTIPLY_1D == 0:
            data1d = [merge_data_tf(data5m[:MULTIPLY_1D])] + data1d
            target_robo.data1d = cut_limit_history(data1d)
            command_list = concat_list(command_list, target_robo.action1d())
        if (i+1) % MULTIPLY_1W == 0:
            data1w = [merge_data_tf(data5m[:MULTIPLY_1W])] + data1w
            target_robo.data1w = cut_limit_history(data1w)
            command_list = concat_list(command_list, target_robo.action1w())
        for command in command_list:
            if command['type'] == CommandType.ORDER:
                new_order_staus = OrderStatus.OPEN
                new_order_filled = 0
                # adjust order base on exchange criteria
                if command['order'] == OrderType.LIMIT:
                    # adjust price
                    if order_spread_usdt[CURRENT_SYMBOL] != None:
                        command["price"] = Decimal(str(round(command['price'], int(
                            math.log10(1/order_spread_usdt[CURRENT_SYMBOL])))))
                    else:
                        continue
                    if min_order_usdt[CURRENT_SYMBOL] != None:
                        if min_order_usdt[CURRENT_SYMBOL] > (Decimal(str(command['qty'])) * Decimal(str(command['price']))):
                            continue
                    else:
                        continue
                if command['order'] == OrderType.MARKET and command['side'] == OrderSide.LONG and ('quote_order_qty' not in command or not command['quote_order_qty']):
                    # 'Robo tried to submit order market for long position with unit quantity, but system does not allow.'
                    continue
                if 'qty' in command:
                    command['qty'] = Decimal(round(Decimal(str(command['qty'])), int(
                        math.log10(1/min_order_amount[CURRENT_SYMBOL]))))
                    # verify command that pass minimum order
                    if min_order_amount[CURRENT_SYMBOL] > command['qty']:
                        # Robo tried to submit order size {} at price {}, which is lower than minimum order size {}
                        continue
                if 'quote_order_qty' in command:
                    command['quote_order_qty'] = Decimal(round(Decimal(str(command['quote_order_qty'])), int(
                        math.log10(1/min_order_usdt[CURRENT_SYMBOL]))))
                    # verify command that pass minimum order
                    if min_order_usdt[CURRENT_SYMBOL] > command['quote_order_qty']:
                        # 'Robo tried to submit order size {} usdt at price {}, which is lower than minimum order size {}
                        continue
                # logic on order type
                if command['order'] == OrderType.LIMIT:
                    if FILL_ORDER_AT_CLOSE_PRICE and command['price'] == target_robo.data5m[0][PriceDataDictColumn.CLOSE]:
                        new_order_staus = OrderStatus.FILLED
                        new_order_filled = command['qty']
                    target_robo.position_list.append({'order_id': running_order_id, 'create_time': int(target_robo.data5m[0][PriceDataDictColumn.OPENTIME]) + 300000, 'price': Decimal(command['price']),
                                                      'side': command['side'], 'status': new_order_staus, 'qty': Decimal(command['qty']), 'sold': 0, 'filled': new_order_filled})
                    running_order_id = running_order_id + 1
                elif command['order'] == OrderType.MARKET:
                    target_robo.position_list.append({'order_id': running_order_id, 'create_time': int(target_robo.data5m[0][PriceDataDictColumn.OPENTIME]) + 300000, 'price': Decimal(target_robo.data5m[0][PriceDataDictColumn.CLOSE]),
                                                      'side': command['side'], 'status':  OrderStatus.FILLED, 'qty': Decimal(command['qty']), 'sold': 0, 'filled': Decimal(command['qty'])})
                    running_order_id = running_order_id + 1
                elif command['order'] == OrderType.CANCEL:
                    for position in target_robo.position_list:
                        if position.status == OrderStatus.OPEN and command_list['order_id'] == position['order_id']:
                            target_robo.position_list.remove(position)
                elif command['order'] == OrderType.CLOSE:
                    close_position_list = []
                    for position in target_robo.position_list:
                        if command_list['order_id'] == position['order_id']:
                            if position.status == OrderStatus.OPEN:
                                target_robo.position_list.remove(position)
                            elif position.status == OrderStatus.FILLED:
                                close_side = OrderSide.SHORT

                                if position['side'] == OrderSide.SHORT:
                                    close_side = OrderSide.LONG
                                close_position_list.append({'order_id': running_order_id, 'create_time': int(target_robo.data5m[0][PriceDataDictColumn.OPENTIME]) + 300000, 'price': target_robo.data5m[0][PriceDataDictColumn.CLOSE],
                                                            'side': close_side, 'status': OrderStatus.FILLED, 'qty': position['qty'] - position['sold'], 'sold': 0, 'filled': position['qty'] - position['sold']})
                                running_order_id = running_order_id + 1
                    target_robo.position_list = target_robo.position_list + close_position_list
            elif command['type'] == CommandType.CLOSE_ALL:
                close_position_list = []
                for position in target_robo.position_list:
                    # for closing -> auto fill on opposite position
                    if position['status'] == OrderStatus.FILLED:
                        close_side = OrderSide.SHORT
                        if position['side'] == OrderSide.SHORT:
                            close_side = OrderSide.LONG
                        close_position_list.append({'order_id': running_order_id, 'create_time': int(target_robo.data5m[0][PriceDataDictColumn.OPENTIME]) + 300000, 'price': target_robo.data5m[0][PriceDataDictColumn.CLOSE],
                                                    'side': close_side, 'status': OrderStatus.FILLED, 'qty': position['qty'] - position['sold'], 'sold': 0, 'filled': position['qty'] - position['sold']})
                        running_order_id = running_order_id + 1
                target_robo.position_list = target_robo.position_list + close_position_list
            elif command['type'] == CommandType.CANCEL_ALL:
                for position in target_robo.position_list:
                    if position['status'] != OrderStatus.FILLED:
                        target_robo.position_list.remove(position)

    print('last fund : ', target_robo.fund)
    print('Running:', timer()-start)
