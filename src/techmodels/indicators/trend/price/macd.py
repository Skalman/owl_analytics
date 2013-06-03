'''
Price Trend Indicator: Moving Average Convergence/Divergence (MACD)
'''
from ma import MAIndicator


class MACDIndicator(object):
    '''
    Moving Average Convergence/Divergence (MACD)
    MACD: (10-period-EMA - 35-period-EMA)
    Signal: 5-period-EMA of MACD
    Indicator: (MACD - Signal)
    '''

    def __init__(self, data, nfast=10, nslow=35, nema=5):
        '''
        Constructor
        data = close prices
        nfast = number of periods for shorter moving average(exponential)
        nslow = number of periods for longer moving average(exponential)
        nema = number of periods for just an exponential moving average
        '''
        self.data = data
        self.nfast = nfast
        self.nslow = nslow
        self.nema = nema
        self.matype = 'exponential'
        self.macd = self.__calculate_macd()

    def __calculate_macd(self):
        return self.emafast() - self.emaslow()

    def emaslow(self):
        return MAIndicator(self.data, self.nslow, self.matype).ma

    def emafast(self):
        return MAIndicator(self.data, self.nfast, self.matype).ma

    def signal(self):
        return MAIndicator(self.macd, self.nema, self.matype).ma

    def indicator(self):
        return self.macd - self.signal()

    def indicator_inverse(self):
        return self.signal() - self.macd
