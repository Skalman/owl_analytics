import numpy as np
from datetime import datetime
import json
import re


class TranformIntradayQuote(object):
    '''Purge, normalize, & convert
    '''

    def __init__(self, marketdata, interval):
        '''Constructor
        '''
        self.marketdata = marketdata
        self.interval = interval
        self.quote = {}
        self.__preprocess()

    def __preprocess(self):
        #####
        #
        # Purge> Harvest header(DCHLOV) & remove metadata
        #
        #####
        def __harvestHeader():
            for i in self.marketdata:
                # search for 'COLUMNS=' only at the start
                if re.search('\ACOLUMNS=', i):
                    return i.split('=')[1].strip('\n').lower()

        def __removeMetadata():
            for i in self.marketdata:
                # matches for 'a' only at the start
                if re.match('\Aa', i):
                    del self.marketdata[0: self.marketdata.index(i)]
                    break

        marketdata_header = [__harvestHeader()]
        __removeMetadata()

        #####
        #
        # Normalize> Split marketdata into: (i)CHLOV & (ii)Date
        #
        #####
        # initialize numpy array size to house CHLOV dataset
        chlov = np.zeros((len(self.marketdata), 5))

        # initialize array to house Date(raw running-timestamps)
        running_ts = []

        # isolate D from CHLOV
        index = 0
        for line in self.marketdata:
            line = line.strip('a')  # normalize initial timestamp
            listFromLine = line.split(',')
            chlov[index, :] = listFromLine[1:6]  # extract CHLOV
            running_ts.append(int(listFromLine[0]))  # extract running-timestamps
            index += 1

        #####
        #
        # Convert> Date(running-timestamps) to: (i)unix-timestamps (ii)datetime-timestamps
        #
        #####
        # initialize arrays to house datetime-timestamp & unix-timestamp
        datetime_ts = []
        unix_ts = []

        def __populateUnix_ts(ts):
            unix_ts.append(ts)

        def __populateDatetime_ts(ts):
            datetime_ts.append(datetime.fromtimestamp(ts))

        def __buildTimeDatasets(ts):
            __populateUnix_ts(ts)
            __populateDatetime_ts(ts)

        # convert running-timestamps to unix-timestamps
        for x in running_ts:
            if x > 500:  # Get the initial timestamp
                    z = x
                    __buildTimeDatasets(x)
            else:
                    y = z + x * int(self.interval)  # multiply the running-timestamps with interval
                    __buildTimeDatasets(y)

        #####
        #
        # Normalize> Merge datasets: (i)CHLOV & (ii)Date
        #
        #####
        def __convertToNpArray(arr):
            na = np.array(arr)
            return na.reshape((len(na), 1))

        def __mergeNpArrays(na1, na2):
            return np.concatenate((na1, na2), axis=1)

        intradayQuote_dts = __mergeNpArrays(__convertToNpArray(datetime_ts), chlov)
        intradayQuote_uts = __mergeNpArrays(__convertToNpArray(unix_ts), chlov)

        self.quote['header'] = marketdata_header
        self.quote['dts_quote'] = intradayQuote_dts
        self.quote['uts_quote'] = intradayQuote_uts

    def __getDCHLOV(self, dateseries):
        q = {}
        q['header'] = self.quote['header']
        q['quote'] = self.quote[dateseries]
        return q

    def __convertToJson(self, quote):
        for line in quote['header']:
            keys = line.split(',')
        data = [{key: val for key, val in zip(keys, prop)}
                    for prop in quote['quote'].tolist()]
        q_json = json.dumps(data)
        return q_json

    def dts_chlov(self):
        return self.__getDCHLOV('dts_quote')

    def uts_chlov(self):
        return self.__getDCHLOV('uts_quote')

    def json_uts_chlov(self):
        q = self.__getDCHLOV('uts_quote')
        return self.__convertToJson(q)
