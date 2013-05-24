import urllib2
import urllib
from marketdata.utils.transform.google.rawquote_intraday import TranformIntradayQuote


def _getUrl(url, urlconditions):
    url_values = urllib.urlencode(urlconditions)
    return url + '?' + url_values


def _pullQuote(url, urlconditions):
    req = urllib2.Request(_getUrl(url, urlconditions))
    response = urllib2.urlopen(req).readlines()
    return response


class IntradayMinutes(object):
    '''Extract intraday market data from Google finance.

    URL to access market data from Google finance:
    http://www.google.com/finance/getprices?q=IBM&x=NYSE&i=60&p=5d&f=d,c,h,l,o,v

    Description of abbreviations present in the above URL:
    q = quote symbol
    x = exchange symbol
    i = interval in seconds i.e. 60 = 1 minute
    p = number of past trading days (max has been 15d)
    f = quote format (date, close, high, low, open, volume)
    '''

    def __init__(self, symbol, exchange, minutes=1, days=1):
        '''Constructor
        '''
        self.url = 'http://www.google.com/finance/getprices'
        quoteformat = 'd,c,h,l,o,v'
        self.urlconditions = {}
        self.urlconditions['q'] = symbol             # 'IBM', 'JPM', 'GE', 'AMD'
        self.urlconditions['x'] = exchange           # 'NYSE', 'INDEXNASDAQ'
        self.urlconditions['i'] = str(minutes * 60)  # 60 refers to 1 minute interval
        self.urlconditions['p'] = str(days) + 'd'    # 1d refers to 1 day (max 15 days)
        self.urlconditions['f'] = quoteformat        # date, close, high, low, open, volume
        self.quote = self.__extractTransform()

    def __extractRawQuote(self):
        return _pullQuote(self.url, self.urlconditions)

    def __transformRawQuote(self, raw_quote):
        interval = self.urlconditions['i']
        return TranformIntradayQuote(raw_quote, interval)

    def __extractTransform(self):
        raw_quote = self.__extractRawQuote()
        return self.__transformRawQuote(raw_quote)

    def json(self):
        return self.quote.json_uts_chlov()

    def dict_np(self):
        return self.quote.dts_chlov()
