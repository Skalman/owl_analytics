'''
Sequential Price-Trend Models: MACD with Price-Bar-Chunk (MDC)
'''
import numpy
import json

from techmodels.overlays.trend.price.chunk import sign_chunker
from techmodels.indicators.trend.price.macd import MACDIndicator


def macd_chunk(data, nfast=10, nslow=35, nema=5, getter=lambda x: x):
    prices = numpy.array(map(getter, data))
    macd_oscillator = MACDIndicator(prices, nfast, nslow, nema)

    # Skip the first nfast values
    cropped_indicator = macd_oscillator.indicator()[nfast + 1:]
    cropped_data = data[nfast + 1:]

    chunks = sign_chunker(cropped_indicator, cropped_data)
    return chunks


def macd_chunk_json(data, pricetype=u'close'):
    python_list = json.loads(data)
    chunks = macd_chunk(python_list, getter=lambda x: x[pricetype])
    return json.dumps(chunks)
