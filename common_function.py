import numpy as np 

def find_column_number(header, target):
    target_pos = -1
    for i in range(len(header)):
        if header[i] == target:
            target_pos = i
            break
    return target_pos

def add_close_open(df, header):
    header.append('close-open')
    df = np.hstack((df, np.transpose([df[:, find_column_number(
        header, 'close-price')]-df[:, find_column_number(header, 'open-price')]])))
    return df, header

def add_high_low(df, header):
    header.append('high-low')
    df = np.hstack((df, np.transpose([df[:, find_column_number(
        header, 'high-price')]-df[:, find_column_number(header, 'low-price')]])))
    return df, header


def add_high_open(df, header):
    header.append('high-open')
    df = np.hstack((df, np.transpose([df[:, find_column_number(
        header, 'high-price')]-df[:, find_column_number(header, 'open-price')]])))
    return df, header


def add_close_low(df, header):
    header.append('close-low')
    df = np.hstack((df, np.transpose([df[:, find_column_number(
        header, 'close-price')]-df[:, find_column_number(header, 'low-price')]])))
    return df, header


def add_ohlc4(df, header):
    header.append('ohlc4')
    ohlc4np = np.zeros((1, len(df)))
    high_price_position = find_column_number(header, 'high-price')
    low_price_position = find_column_number(header, 'low-price')
    open_price_position = find_column_number(header, 'open-price')
    close_price_position = find_column_number(header, 'close-price')
    for i in range(len(df)):
        ohlc4np[0][i] = (df[i][high_price_position] + df[i][low_price_position] + df[i][open_price_position] + df[i][close_price_position]) / 4
    df = np.hstack((df, np.transpose(ohlc4np)))
    return df, header