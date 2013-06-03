'''
Price Trend Indicator: Moving Average (MA)
'''
import numpy


class MAIndicator(object):
    '''
    Moving Average(MA)
    SMA: (summation of all N-period-prices / N)
    EMA: exponential of all N-period-prices
    Indicator: -None-
    '''

    def __init__(self, data, n, t='simple'):
        '''
        Constructor
        data = close prices
        n = number of periods
        t(type) = 'simple' | 'exponential'
        '''
        self.data = data
        self.n = n
        self.t = t
        self.ma = self.__calculate_ma()

    def __calculate_ma(self):
        self.data = numpy.asarray(self.data)
        if self.t == 'simple':
            weights = numpy.ones(self.n)
        else:
            weights = numpy.exp(numpy.linspace(-1., 0., self.n))

        weights /= weights.sum()
        a = numpy.convolve(self.data, weights, mode='full')[:len(self.data)]
        a[:self.n] = a[self.n]
        return a
