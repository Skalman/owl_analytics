import numpy
import math
import json

def moving_average(p, n, type='simple'):
	"""
	compute an n period moving average.

	type is 'simple' | 'exponential'
	"""
	p = numpy.asarray(p)
	if type=='simple':
		weights = numpy.ones(n)
	else:
		weights = numpy.exp(numpy.linspace(-1., 0., n))

	weights /= weights.sum()


	a = numpy.convolve(p, weights, mode='full')[:len(p)]
	a[:n] = a[n]
	return a

def moving_average_convergence(p, nslow=26, nfast=12):
	"""
	compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
	return value is emaslow, emafast, macd which are len(p) arrays
	"""
	emaslow = moving_average(p, nslow, type='exponential')
	emafast = moving_average(p, nfast, type='exponential')
	return emaslow, emafast, emafast - emaslow

# TODO: move to sign_chunker
def macd_chunk(data, nfast = 10, nslow = 35, nema = 5, return_all = False, getter = lambda x: x):
	prices = numpy.array( map(getter, data) )

	emaslow, emafast, macd = moving_average_convergence(prices, nslow=nslow, nfast=nfast)
	ema9 = moving_average(macd, nema, type='exponential')

	y1 = macd-ema9
	y2 = ema9-macd

	chunks = []

	next_chunk_begin_index = nfast+1
	cursign = -1 if y1[next_chunk_begin_index] < 0 else 1

	# Skip the first nfast values
	for x in range(nfast+1, len(y1)):
		this_sign = -1 if y1[x] < 0 else 1

		if this_sign != cursign:
			chunks.append({
				'sign': cursign,
				'data': data[next_chunk_begin_index:x],
			})
			next_chunk_begin_index = x
			cursign = this_sign

	if return_all:
		return {
			'prices': prices,
			'chunks': chunks,
			'emaslow': emaslow,
			'emafast': emafast,
			'macd': macd,
			'y1': y1,
			'y2': y2,
		}
	else:
		return chunks


def macd_chunk_json(input):
	python_list = json.loads(input)
	chunks = macd_chunk(python_list, getter = lambda x: x[u'close'])
	return json.dumps(chunks)
