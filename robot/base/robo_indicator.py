import numpy as np
import math


def calculate_ma(datadict_array, value_column, ma_column, ma_level):
    sum_value = 0.0
    first_ma_value = 0.0
    data_dict_len = len(datadict_array)
    skip_nan = 0
    for i in range(data_dict_len):
        if math.isnan(datadict_array[data_dict_len-1-i][value_column]):
            skip_nan = skip_nan + 1
        else:
            break

    if ma_level + skip_nan >= data_dict_len:
        for i in range(data_dict_len):
            datadict_array[i][ma_column] = float('nan')
    else:
        # replace nan to could not calcualte because of source is nan
        for i in range(skip_nan):
            datadict_array[data_dict_len-1-i][ma_column] = float('nan')
        for i in range(ma_level):
            if i == 0:
                first_ma_value = datadict_array[data_dict_len -
                                                1-i-skip_nan][value_column]
            sum_value = sum_value + \
                datadict_array[data_dict_len-1-i-skip_nan][value_column]
            datadict_array[data_dict_len-1-i -
                           skip_nan][ma_column] = float('nan')
        datadict_array[data_dict_len -
                       ma_level - skip_nan][ma_column] = sum_value / ma_level

        for i in range(data_dict_len-ma_level-skip_nan):
            sum_value = sum_value - first_ma_value + \
                datadict_array[data_dict_len -
                               ma_level-1-i-skip_nan][value_column]
            datadict_array[data_dict_len-ma_level-1-i -
                           skip_nan][ma_column] = sum_value / ma_level
    return datadict_array


def calculate_ema(datadict_array, value_column, ema_column, ema_level):
    # EMA: {Close - EMA(previous day)} x multiplier + EMA(previous day).
    # first value of EMA will equal to MA(ema_level)
    sum_value = 0.0
    data_dict_len = len(datadict_array)
    skip_nan = 0
    for i in range(data_dict_len):
        if math.isnan(datadict_array[data_dict_len-1-i][value_column]):
            skip_nan = skip_nan + 1
        else:
            break

    if ema_level + skip_nan >= data_dict_len:
        for i in range(data_dict_len):
            datadict_array[i][ema_column] = float('nan')
    else:
        # replace nan to could not calcualte because of source is nan
        for i in range(skip_nan):
            datadict_array[data_dict_len-1-i][ema_column] = float('nan')
        for i in range(ema_level):
            sum_value = sum_value + \
                datadict_array[data_dict_len-1-i-skip_nan][value_column]
            datadict_array[data_dict_len-1-i -
                           skip_nan][ema_column] = float('nan')
        datadict_array[data_dict_len -
                       ema_level - skip_nan][ema_column] = sum_value / ema_level

        for i in range(data_dict_len-ema_level-skip_nan):
            alpha = 2 / (ema_level + 1)  # multiplier
            datadict_array[data_dict_len-ema_level-1-i-skip_nan][ema_column] = alpha * (datadict_array[data_dict_len-ema_level-1-i-skip_nan][value_column] -
                                                                                        datadict_array[data_dict_len-ema_level-i-skip_nan][ema_column]) + datadict_array[data_dict_len-ema_level-i-skip_nan][ema_column]
    return datadict_array
