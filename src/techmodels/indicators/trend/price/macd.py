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

    def __init__(self, nfast=10, nslow=35, nema=5):
        '''
        Constructor
        data = close prices
        nfast = number of periods for shorter moving average(exponential)
        nslow = number of periods for longer moving average(exponential)
        nema = number of periods for just an exponential moving average
        '''
        self.nfast = nfast
        self.nslow = nslow
        self.nema = nema
        self.matype = 'exponential'

    def macd(self, data):
        return self.emafast(data) - self.emaslow(data)

    def emaslow(self, data):
        return MAIndicator(self.nslow, self.matype).ma(data)

    def emafast(self, data):
        return MAIndicator(self.nfast, self.matype).ma(data)

    def signal(self, data):
        return MAIndicator(self.nema, self.matype).ma(self.macd(data))

    def indicator(self, data):
        return self.macd(data) - self.signal(data)

    def indicator_inverse(self, data):
        return self.signal(data) - self.macd(data)
