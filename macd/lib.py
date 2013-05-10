import numpy

def moving_average(p, n, type = 'simple'):
	"""
	compute an n period moving average.

	type is 'simple' | 'exponential'
	"""
	p = numpy.asarray(p)
	if type == 'simple':
		weights = numpy.ones(n)
	else:
		weights = numpy.exp(numpy.linspace(-1., 0., n))

	weights /= weights.sum()

	a = numpy.convolve(p, weights, mode = 'full')[:len(p)]
	a[:n] = a[n]
	return a


def moving_average_convergence(p, nfast = 10, nslow = 35):
	"""
	compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
	return value is emaslow, emafast, macd which are len(p) arrays
	"""
	emaslow = moving_average(p, nslow, type = 'exponential')
	emafast = moving_average(p, nfast, type = 'exponential')
	return emaslow, emafast, emafast - emaslow


def macd(data, nfast = 10, nslow = 35, nema = 5, return_all = False):
	
	emaslow, emafast, macd = moving_average_convergence(data, nslow=nslow, nfast=nfast)
	ema9 = moving_average(macd, nema, type='exponential')

	y1 = macd-ema9
	y2 = ema9-macd

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
