from ta.trend import EMAIndicator,SMAIndicator
import pandas as pd

def calculate_ma(datadict_array, value_column, ma_column, ma_level):
    df = pd.DataFrame(data=datadict_array)
    df = df.iloc[::-1]
    result_ema = SMAIndicator(close=df[value_column], window=ma_level, fillna=False).sma_indicator().iloc[::-1].to_dict()
    for i in range(len(datadict_array)) :
        datadict_array[i][ma_column] = result_ema[i]
    return datadict_array


def calculate_ema(datadict_array, value_column, ema_column, ema_level):
    df = pd.DataFrame(data=datadict_array)
    df = df.iloc[::-1]
    result_ema = EMAIndicator(close=df[value_column], window=ema_level, fillna=False).ema_indicator().iloc[::-1].to_dict()
    for i in range(len(datadict_array)) :
        datadict_array[i][ema_column] = result_ema[i]
    return datadict_array
