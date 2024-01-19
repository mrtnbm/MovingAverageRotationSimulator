import pandas as pd


class TechnicalIndicators:
    @staticmethod
    def get_moving_average(values, window_size, type='sma'):
        if type == 'sma':
            return TechnicalIndicators.get_simple_moving_average(values, window_size).tolist()
        elif type == 'ema':
            return TechnicalIndicators.get_exponential_moving_average(values, window_size).tolist()
        else:
            raise ValueError('Invalid moving average type')
    
    @staticmethod
    def get_multi_index_moving_average(values_lists, index_weights, window_size, type='sma'):
        ma = 0
        for j in range(len(index_weights)):
            if type == 'sma':
                ma += TechnicalIndicators.get_simple_moving_average(values_lists[j], window_size).multiply(index_weights[j])
            elif type == 'ema':
                ma += index_weights[j] * TechnicalIndicators.get_exponential_moving_average(values_lists[j], window_size).multiply(index_weights[j])
            else:
                raise ValueError('Invalid moving average type')
        return ma.tolist()
    
    @staticmethod
    def get_simple_moving_average(values, window_size):
        return pd.Series(values).rolling(window=window_size).mean()

    @staticmethod
    def get_exponential_moving_average(values, window_size):
        return pd.Series(values).ewm(span=window_size, adjust=False).mean()