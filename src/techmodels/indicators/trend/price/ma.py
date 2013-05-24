'''
Price Trend Indicator: Moving Average (MA)
'''
import numpy


def moving_average(p, n, t='simple'):
    """
    compute an n period moving average.

    t(type) is 'simple' | 'exponential'
    """
    p = numpy.asarray(p)
    if t == 'simple':
        weights = numpy.ones(n)
    else:
        weights = numpy.exp(numpy.linspace(-1., 0., n))

    weights /= weights.sum()

    a = numpy.convolve(p, weights, mode='full')[:len(p)]
    a[:n] = a[n]
    return a
