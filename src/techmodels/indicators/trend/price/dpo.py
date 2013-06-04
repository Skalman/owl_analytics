'''
Price Trend Indicator: Detrended Price Oscillator (DPO)
'''
from ma import MAIndicator
import numpy as np


class DPOIndicator(object):
    '''
    Detrended Price Oscillator (DPO)
    Price = (10/2)+1 period ago price
    SMA = 10-period-SMA
    Indicator: (Price - SMA)
    '''

    def __init__(self, n=10):
        '''
        Constructor
        data = close prices
        n = number of periods
        '''
        self.n = n
        self.shifted_period = (n / 2 + 1)  # TODO think about Python 3!!!

    def indicator(self, data):
        dpo = self.__shiftdata(data) - self.sma(data)[self.shifted_period:]
        return dpo

    def indicator_inverse(self, data):
        dpo = self.sma(data)[self.shifted_period:] - self.__shiftdata(data)
        return dpo

    def sma(self, data):
        sma = MAIndicator(self.n, t='simple').ma(data)
        return self.__fill_nan(sma)

    def __shiftdata(self, data):
        shifteddata = self.__fill_nan(data[self.shifted_period:])
        return shifteddata

    def __fill_nan(self, arr):
        displaced_items = np.ndarray((self.shifted_period,))
        displaced_items.fill(np.NaN)
        arr = np.append(arr, displaced_items)
        return arr
