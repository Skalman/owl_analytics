"""
Source Code Origin: http://nighttimecuriosities.blogspot.fi/2012/08/historical-intraday-stock-price-data.html
"""

import urllib2
import urllib
import numpy as np
from datetime import datetime
import csv
import json
from macd.macd_chunker import macd_chunk_json, macd_chunk

urldata = {} 
urldata['q'] = ticker = 'JPM'       # stock symbol
urldata['x'] = 'NYSE'               # exchange symbol
urldata['i'] = '60'                 # interval
urldata['p'] = '1d'                 # number of past trading days (max has been 15d)
urldata['f'] = 'd,o,h,l,c,v'        # requested data d is time, o is open, c is closing, h is high, l is low, v is volume
 
url_values = urllib.urlencode(urldata)
url = 'http://www.google.com/finance/getprices'
full_url = url + '?' + url_values
req = urllib2.Request(full_url)
response = urllib2.urlopen(req).readlines()
getdata = response

# get marketdata header(DOHCLV)
del getdata[0:4]
del getdata[1:3]
marketdata_header = [getdata[0].split('=')[1].lower()]

# preprocess DOHCLV marketdata
del getdata[0:1]
numberoflines = len(getdata)
returnMat = np.zeros((numberoflines, 5))
timeVector = []
timeVector_UnixTimestamp = []
 
index = 0
for line in getdata:
	line = line.strip('a')
	listFromLine = line.split(',')
	returnMat[index,:] = listFromLine[1:6]
	timeVector.append(int(listFromLine[0]))
	timeVector_UnixTimestamp.append(int(listFromLine[0]))
	index += 1

# convert Unix or epoch timestamp to datetime-timestamp
for x in timeVector:
	if x > 500:
		z = x
		timeVector[timeVector.index(x)] = datetime.fromtimestamp(x)
		timeVector_UnixTimestamp[timeVector_UnixTimestamp.index(x)] = x
	else:
		y = z+x*int(urldata['i']) # multiply by interval
		timeVector[timeVector.index(x)] = datetime.fromtimestamp(y)
		timeVector_UnixTimestamp[timeVector_UnixTimestamp.index(x)] = y
 
tdata = np.array(timeVector)
tdata_UnixTimestamp = np.array(timeVector_UnixTimestamp)

time = tdata.reshape((len(tdata),1))
time_UnixTimestamp = tdata_UnixTimestamp.reshape((len(tdata_UnixTimestamp),1))

# Numpy Array market-dataset with datetime formated timestamp
intradata = np.concatenate((time, returnMat), axis=1)

# Numpy Array market-dataset with Unix formated timestamp
intradata_UnixTimestamp = np.concatenate((time_UnixTimestamp, returnMat), axis=1)

# convert to JSON from Numpy Array dataset with UnixTimestamp
# resutling JSON formate => [{"volume": 400.0, "high": 49.08, "low": 49.05, "date": 1367242200.0, "close": 49.05, "open": 49.08}]
mdHeader = csv.reader(marketdata_header, delimiter=',')
keys = next(mdHeader)
mdList = [{key: val for key, val in zip(keys, prop)} for prop in intradata_UnixTimestamp.tolist()]



# convert to JSON from Numpy Array dataset with UnixTimestamp
# resutling JSON formate => [{"volume": 400.0, "high": 49.08, "low": 49.05, "date": 1367242200.0, "close": 49.05, "open": 49.08}]
mdHeader = csv.reader(marketdata_header, delimiter=',')
keys = next(mdHeader)
mdList = [{key: val for key, val in zip(keys, prop)} for prop in intradata_UnixTimestamp.tolist()]
intradata_json = json.dumps(mdList)

#macd_chunk_json(intradata_json)

all_chunked = macd_chunk(mdList, nfast = 10, nslow = 35, nema = 5, getter = lambda x: x[u'close'], return_all = True)
mChunk = all_chunked['chunks']
#print mChunk
t_mChunk_up = []
t_mChunk_down = []
flag_mChunk_up = []
flag_mChunk_down = []
ymin_mChunk_up = 0 
ymin_mChunk_down = 0 
ymax_mChunk_up = 0
ymax_mChunk_down = 0
for i in mChunk:
	if i['sign'] == 1:
		#print '+ve'
		dates = map(lambda x: x[u'date'], i['data'])
		t_mChunk_up.append(datetime.fromtimestamp(dates[0]))
		flag_mChunk_up.append(False)
		t_mChunk_up.append(datetime.fromtimestamp(dates[0]))
		flag_mChunk_up.append(True)
		t_mChunk_up.append(datetime.fromtimestamp(dates[-1]))
		flag_mChunk_up.append(True)
		t_mChunk_up.append(datetime.fromtimestamp(dates[-1]))
		flag_mChunk_up.append(False)
		ymin_mChunk_up = min(map(lambda x: x[u'low'], i['data']))
		ymax_mChunk_up = max(map(lambda x: x[u'high'], i['data']))
	else:
		#print '-ve'
		dates = map(lambda x: x[u'date'], i['data'])
		t_mChunk_down.append(datetime.fromtimestamp(dates[0]))
		flag_mChunk_down.append(True)
		t_mChunk_down.append(datetime.fromtimestamp(dates[-1]))
		flag_mChunk_down.append(True)
		t_mChunk_down.append(datetime.fromtimestamp(dates[-1]))
		flag_mChunk_down.append(False)
		ymin_mChunk_down = min(map(lambda x: x[u'low'], i['data']))
		ymax_mChunk_down = max(map(lambda x: x[u'high'], i['data']))

