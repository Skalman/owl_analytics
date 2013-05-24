import marketdata.access.remote.google as quoteresource


def getQuote(s):
    return quoteresource.IntradayMinutes(symbol=s,
                                          exchange='NYSE',
                                          minutes=1,
                                          days=1)
intradaydata = getQuote('IBM')
intradaydata_np = intradaydata.dict_np()['quote']
intradaydata_json = intradaydata.json()
#print intradaydata_np
