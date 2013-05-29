import numpy as np
from datetime import datetime
import json
import re


class TranformIntradayQuote(object):
    '''Purge, normalize, & convert data within raw quote.
    '''

    def __init__(self, rawquote, interval):
        '''Constructor
        '''
        self.rawquote = rawquote
        self.interval = interval
        self.quote = {}
        self.__preprocess()

    def __preprocess(self):
        # purge action: harvest header(DCHLOV) & remove the metadata
        quote_header = [self.__harvestHeader()]
        self.__removeMetadata()

        # normalization action: isolate DCHLOV into two parts: (i)D & (ii)CHLOV
        i = self.__isolateDateFromCHLOV()
        running_ts = i[0]
        chlov = i[1]

        # conversion action: D to (i)unix(uts) & (ii)datetime(dts)
        timestamps = self.__uts_dts(running_ts)
        unix_ts = timestamps[0]
        datetime_ts = timestamps[1]

        # normalization action: merge datasets (i)D & (ii)CHLOV
        intradayQuote_dts = self.__mergeNpArrays(
                                self.__convertToNpArray(datetime_ts), chlov)
        intradayQuote_uts = self.__mergeNpArrays(
                                self.__convertToNpArray(unix_ts), chlov)

        # produce quote with (i)header (ii)DCHLOV(dts) & (iii)DCHLOV(uts)
        self.quote['header'] = quote_header
        self.quote['dts_quote'] = intradayQuote_dts
        self.quote['uts_quote'] = intradayQuote_uts

    def __harvestHeader(self):
            for i in self.rawquote:
                # search for 'COLUMNS=' only at the start of a string
                if re.search('\ACOLUMNS=', i):
                    return i.split('=')[1].strip('\n').lower()

    def __removeMetadata(self):
        for i in self.rawquote:
            # matches for 'a' only at the start of a string
            if re.match('\Aa', i):
                del self.rawquote[0: self.rawquote.index(i)]
                break

    def __isolateDateFromCHLOV(self):
        # initialize numpy array for CHLOV dataset
        chlov = np.zeros((len(self.rawquote), 5))

        # initialize array for D(running-timestamps) dataset
        running_ts = []

        # isolate D from CHLOV
        index = 0
        for line in self.rawquote:
            line = line.strip('a')  # normalize the very first timestamp
            listFromLine = line.split(',')
            chlov[index, :] = listFromLine[1:6]  # extract CHLOV
            running_ts.append(int(listFromLine[0]))  # extract D
            index += 1
        return [running_ts, chlov]

    def __uts_dts(self, running_ts):
        # initialize arrays for datetime-timestamp & unix-timestamp datasets
        dts = []
        uts = []

        def __populateUTS(ts):
            uts.append(ts)

        def __populateDTS(ts):
            dts.append(datetime.fromtimestamp(ts))

        def __buildTimeDatasets(ts):
            __populateUTS(ts)
            __populateDTS(ts)

        # convert running-timestamp to unix-timestamp
        for x in running_ts:
            if x > 500:  # get the initial timestamp
                    z = x
                    __buildTimeDatasets(x)
            else:
                    y = z + x * int(self.interval)
                    __buildTimeDatasets(y)
        return [uts, dts]

    def __convertToNpArray(self, arr):
        na = np.array(arr)
        return na.reshape((len(na), 1))

    def __mergeNpArrays(self, a, b):
        return np.concatenate((a, b), axis=1)

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
