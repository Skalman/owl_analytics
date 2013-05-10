import numpy
import math
import json

from chunker.sign_chunker import sign_chunker

from macd.lib import macd


def macd_chunk(data, nfast = 10, nslow = 35, nema = 5, return_all = False, getter = lambda x: x):
	prices = numpy.array( map(getter, data) )

	calculated = macd(prices, nfast = nfast, nslow = nslow, nema = nema, return_all = True)
	y1 = calculated['y1']

	# Skip the first nfast values

	# Note: could use a list view instead to save memory, but it might be less efficient
	# See: http://stackoverflow.com/questions/3485475/can-i-create-a-view-on-a-python-list#3485490
	cropped_y1 = y1[nfast+1:]
	cropped_data = data[nfast+1:]
	
	chunks = sign_chunker(cropped_y1, cropped_data)

	if return_all:
		calculated['prices'] = prices
		calculated['chunks'] = chunks
		return calculated
	else:
		return chunks


def macd_chunk_json(input):
	python_list = json.loads(input)
	chunks = macd_chunk(python_list, getter = lambda x: x[u'close'])
	return json.dumps(chunks)
