from ta.trend import EMAIndicator, SMAIndicator
import pandas as pd

#ma_column, ma_level
def calculate_ma(datadict_array, value_column, ma_request):
    df = pd.DataFrame(data=datadict_array)
    df = df.iloc[::-1]
    result_ma = {}
    for i in range(len(ma_request)) : 
        result_ma['result' + str(i) ] = SMAIndicator(
            close=df[value_column], window=ma_request[i]['ma_level'], fillna=False).sma_indicator().iloc[::-1].to_dict()
    for i in range(len(datadict_array)):
        for j in range(len(ma_request)) : 
            datadict_array[i][ma_request[j]['ma_column']] = result_ma['result' + str(j)][i]
    return datadict_array


def calculate_ema(datadict_array, value_column: str, ema_request) :
    df = pd.DataFrame(data=datadict_array)
    df = df.iloc[::-1]
    result_ema = {}
    for i in range(len(ema_request)) : 
        result_ema['result' + str(i) ] = EMAIndicator(
            close=df[value_column], window=ema_request[i]['ema_level'], fillna=False).ema_indicator().iloc[::-1].to_dict()
    for i in range(len(datadict_array)):
        for j in range(len(ema_request)) : 
            datadict_array[i][ema_request[j]['ema_column']] = result_ema['result' + str(j)][i]
    return datadict_array
