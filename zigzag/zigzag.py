# Hi-n-lo - filter out the highs and the lows
# Copyright (C) 2013  Dan Wolff
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


def all(data, getter=lambda x: x):
    '''Get all highs and lows

    Get all highs and lows. The resulting array is guaranteed to alternate
    between highs and lows.
    '''
    if len(data) <= 1:
        # return a copy of the list
        return data[:]

    last = data[0]
    result = [last]

    for i in range(1, len(data) - 1):
        # figure out whether to keep y
        x = getter(last)
        y = getter(data[i])
        z = getter(data[i + 1])
        if x <= y <= z or x >= y >= z:
            # nothing happens
            pass
        else:
            last = data[i]
            result.append(last)

    result.append(data[-1])
    return result


def min_change(data, change=10, type='percent', getter=lambda x: x):
    '''(list, change=<num>, type='percent' | 'absolute', getter=lambda) -> list
    Return highs and lows, filtered by sensitivity.

    Given an array, this function returns an array that is guaranteed to
    alternate between highs and lows. Additionally, variations smaller than
    `sensitivity` are removed.
    '''
    result = all(data, getter=getter)

    length = len(result)

    def get_absolute_change(b, c):
        return abs(c - b)

    def get_relative_change(b, c):
        if b < c:
            return 100 * (1 - float(b) / c)
        else:
            return 100 * (1 - float(c) / b)

    if type == 'percent':
        assert 0 <= change <= 100
        get_change = get_relative_change
    elif type == 'absolute':
        assert 0 <= change
        get_change = get_absolute_change
    else:
        assert type == 'percent' or type == 'absolute'

    i = length - 4
    while i >= 0:
        # Use four points a-b-c-d to figure out whether we can safely remove b
        # and c
        a = getter(result[i])
        b = getter(result[i + 1])
        c = getter(result[i + 2])
        d = getter(result[i + 3])

        # Check whether b and c are middle points
        if b < c:
            # is a the highest and d the lowest?
            middle_points = a >= c and b >= d
        else:
            # is a the lowest and d the highest?
            middle_points = a <= c and b <= d

        if middle_points and get_change(b, c) < change:
            # remove
            del result[i + 1:i + 3]
            i -= 2
        else:
            i -= 1

    return result


def max_points(data, points=2, type='percent', getter=lambda x: x, return_min_change=False):
    '''
    1. Find all high and low points
    2. Calculate changes between the points
    3. Loop:
        a. If the number of points (remaining) is less than or equal to the desired amount of points, break out of the loop
        b. Find the smallest change
        c. Remove the points which create that change
        d. Recalculate the change around the removed points
    4. The smallest remaining change is now the minimum change


    Potential optimizations to look into, in order to go from
    O(n^2) to O(n*log(n)):

    * Use a linked list to enable quick deletions from the list
    * Consider whether it could be possible to remove multiple points in one go.
      It might be possible to remove the smallest half of the changes in one go.
      Currently, only two points are removed.
    '''

    assert type == 'percent'  # absolute not supported at this point

    zz = all(data, getter=getter)

    def get_relative_change(b, c):
        '''
        Returns a number between 0 and 1 (0 is no change, 1 is 100% change)
        '''
        if b < c:
            return 1 - float(b) / c
        else:
            return 1 - float(c) / b

    def index_of_smallest_except_edge(iter):
        '''
        Find the smallest value in a list, but the first and the last item are
        ignored. Return the index of the value in question.

        >>> index_of_smallest_except_edge([1, 6, 8, 2, 6, 3, 8])
        3
        '''
        index = 1
        for x in range(2, len(iter) - 1):
            if iter[x] < iter[index]:
                index = x
        return index

    # Calculate the changes between all the points
    changes = []
    for x in range(0, len(zz) - 1):
        changes.append(get_relative_change(getter(zz[x]), getter(zz[x + 1])))

    while points + 2 <= len(zz):
        # Find the smallest change
        s = index_of_smallest_except_edge(changes)

        # Calculate the new change for the surrounding points
        new_change = get_relative_change(getter(zz[s - 1]), getter(zz[s + 2]))

        # Remove the two points which created the smallest change (s and s+1)
        del zz[s:s + 2]

        # Replace three changes with one recalculated (s-1, s and s+1)
        changes[s - 1:s + 2] = [new_change]

    # Remove the edge values
    zz = zz[1:-1]

    if return_min_change:
        return {
            'data': zz,
            'min_change': changes[index_of_smallest_except_edge(changes)],
        }
    else:
        return zz
