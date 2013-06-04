'''
Sequential Price-Trend Models: DPO with Price-Bar-Chunk (DPC)
'''
import numpy
import json

from techmodels.overlays.trend.price.chunk import sign_chunker
from techmodels.indicators.trend.price.dpo import DPOIndicator


def dpo_chunk(data, n=10, getter=lambda x: x):
    prices = numpy.array(map(getter, data))
    dpo = DPOIndicator(n)
    chunks = sign_chunker(dpo.indicator(prices), data)
    return chunks


def macd_chunk_json(data, pricetype=u'close'):
    python_list = json.loads(data)
    chunks = dpo_chunk(python_list, getter=lambda x: x[pricetype])
    return json.dumps(chunks)
