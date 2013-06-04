

class ChunkOverlay(object):
    def __init__(self, include_last=False):
        self.__include_last = include_last

    def __sign(self, num, zero):
        if num > 0:
            return 1
        elif num < 0:
            return -1
        else:
            return zero

    def sign(self, data, return_data=None):
        '''Chunks a list by the sign.

        >>> ChunkOverlay().sign([1, 2, -3, -4, 5])
        [{'data': [1, 2],   'sign':  1},
         {'data': [-3, -4], 'sign': -1}]

        >>> ChunkOverlay().sign([0, 0, -1, 0, 2])
        [{'data': [0, 0, -1, 0], 'sign': -1}]

        >>> ChunkOverlay(include_last = True).sign([5, -5])
        [{'data': [5],  'sign':  1},
         {'data': [-5], 'sign': -1}]

        >>> ChunkOverlay(include_last = True).sign([])
        []

        >>> ChunkOverlay(include_last = True).sign([1, 2])
        [{'data': [1, 2], 'sign': 1}]
        '''
        if return_data is None:
            return_data = data

        chunks = []

        begin_index = 0
        cur_sign = 0
        last_sign = 0

        for x in range(len(data)):
            cur_sign = self.__sign(data[x], zero=last_sign)

            if cur_sign != last_sign:
                if last_sign != 0:
                    chunks.append({
                        'sign': -cur_sign,
                        'data': return_data[begin_index:x],
                    })
                    begin_index = x
                last_sign = cur_sign

        if self.__include_last and len(data) > 0:
            chunks.append({
                'sign': cur_sign,
                'data': return_data[begin_index:]
            })

        return chunks

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
