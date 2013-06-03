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

    def __init__(self, data, n=10):
        '''
        Constructor
        data = close prices
        n = number of periods
        '''
        self.data = data
        self.n = n
        self.shifted_period = (n / 2 + 1)

    def indicator(self):
        dpo = self.__shiftdata() - self.sma()[self.shifted_period:]
        return dpo

    def indicator_inverse(self):
        dpo = self.sma()[self.shifted_period:] - self.__shiftdata()
        return dpo

    def sma(self):
        sma = MAIndicator(self.data, self.n, t='simple').ma
        return self.__fill_nan(sma)

    def __shiftdata(self):
        shifteddata = self.__fill_nan(self.data[self.shifted_period:])
        return shifteddata

    def __fill_nan(self, arr):
        displaced_items = np.ndarray((self.shifted_period,))
        displaced_items.fill(np.NaN)
        arr = np.append(arr, displaced_items)
        return arr
