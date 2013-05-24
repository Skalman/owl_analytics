'''
Price Trend Indicator: Moving Average Convergence/Divergence (MACD)
'''
from ma import moving_average


def moving_average_convergence(p, nfast=10, nslow=35):
    '''compute the MACD (Moving Average Convergence/Divergence) using a fast
    and slow exponential moving avgerages.
    return value is emaslow, emafast, macd which are len(p) arrays
    '''
    emaslow = moving_average(p, nslow, t='exponential')
    emafast = moving_average(p, nfast, t='exponential')
    return emaslow, emafast, emafast - emaslow


def macd(data, nfast=10, nslow=35, nema=5, return_all=False):
    emaslow, emafast, macd = moving_average_convergence(data,
                                                        nslow=nslow,
                                                        nfast=nfast)
    ema9 = moving_average(macd, nema, t='exponential')

    y1 = macd - ema9
    y2 = ema9 - macd

    if return_all:
        return {
            'macd': macd,
            'emaslow': emaslow,
            'emafast': emafast,
            'ema9': ema9,
            'y1': y1,
            'y2': y2,
        }
    else:
        return y1
