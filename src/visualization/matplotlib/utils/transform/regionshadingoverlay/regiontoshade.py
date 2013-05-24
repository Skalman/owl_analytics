from datetime import datetime


class TranformRegionToShade(object):
    '''Generate region to shade dataset
    '''

    def __init__(self, oscillations):
        '''Constructor
        '''
        self.oscillations = oscillations
        self.positiveRegion = {'timestamp': [], 'flag': [],
                               'ymin': None, 'ymax': None}
        self.negativeRegion = {'timestamp': [], 'flag': [],
                               'ymin': None, 'ymax': None}
        self.__preprocess()

    def __preprocess(self):
        def __fillRegionalPoints(phase, ts, flag):
            if phase == 'positive':
                self.positiveRegion['timestamp'].append(ts)
                self.positiveRegion['flag'].append(flag)
            else:
                self.negativeRegion['timestamp'].append(ts)
                self.negativeRegion['flag'].append(flag)

        def __generateRegion(phase, data):
            dates = map(lambda x: x[u'date'], data['data'])
            startpoint = datetime.fromtimestamp(dates[0])
            endpoint = datetime.fromtimestamp(dates[-1])
            timestamps = [startpoint, endpoint]
            isolationpoint = None
            for ts in timestamps:
                __fillRegionalPoints(phase, ts, True)
                isolationpoint = ts
            __fillRegionalPoints(phase, isolationpoint, False)

        for i in self.oscillations:
            # +ve oscillation phase
            if i['sign'] == 1:
                __generateRegion('positive', i)
                self.positiveRegion['ymin'] = min(map(lambda x: x[u'low'], i['data']))
                self.positiveRegion['ymax'] = max(map(lambda x: x[u'high'], i['data']))

            # -ve oscillation phase
            else:
                __generateRegion('negative', i)
                self.negativeRegion['ymin'] = min(map(lambda x: x[u'low'], i['data']))
                self.negativeRegion['ymax'] = max(map(lambda x: x[u'high'], i['data']))

    def positiveFlag(self):
        return self.positiveRegion['flag']

    def positiveTimestamps(self):
        return self.positiveRegion['timestamp']

    def positiveYmin(self):
        return self.positiveRegion['ymin']

    def positiveYmax(self):
        return self.positiveRegion['ymax']

    def negativeFlag(self):
        return self.negativeRegion['flag']

    def negativeTimestamps(self):
        return self.negativeRegion['timestamp']

    def negativeYmin(self):
        return self.negativeRegion['ymin']

    def negativeYmax(self):
        return self.negativeRegion['ymax']
