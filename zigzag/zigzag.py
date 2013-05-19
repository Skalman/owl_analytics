#! /usr/bin/env python


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


# Example usage
# -------------
# The two variants will do the exact same thing:
# ./zigzag.py -s 0.03 < data/marketdata.csv > data/marketdata-filtered.csv
# ./zigzag.py -s 0.03 -i data/marketdata.csv -o data/marketdata-filtered.csv


import sys
import csv
import argparse


def main():
    # argument parsing
    parser = argparse.ArgumentParser(description='find hi and lo values')
    parser.add_argument('-i, --input-file', metavar='<file>', type=str,
                        dest='input',
                        help='input file (default: stdin)')

    parser.add_argument('-o, --output-file', metavar='<file>', type=str,
                        dest='output',
                        help='output file (default: stdout)')

    parser.add_argument(
        '-s, --sensitivity', metavar='<num>', default=0, type=float,
        dest='sensitivity',
        help='sensitivity, a non-negative number (default: 0)')

    args = parser.parse_args()

    data = []
    header = None

    if args.input == None or args.input == '-':
        input = sys.stdin
    else:
        input = open(args.input, 'r')

    if args.output == None or args.output == '-':
        output = sys.stdout
    else:
        output = open(args.output, 'w')

    # read from file
    csvreader = csv.reader(input, delimiter=',', quotechar='|')

    is_first = True
    for row in csvreader:
        if is_first:
            # the first row contains the header
            header = row
            is_first = False
        else:
            data.append((row[0], float(row[1])))

    # calculate
    zigzag = get_zigzag(data, getter=lambda x: x[1],
                        sensitivity=args.sensitivity)

    # write to file
    csvwriter = csv.writer(
        output, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(header)
    csvwriter.writerows(zigzag)


def get_zigzag(arr, absolute_sensitivity=0, relative_sensitivity=0, getter=lambda x: x):
    if absolute_sensitivity == 0 and relative_sensitivity == 0:
        return get_all_zigzag(arr, getter=getter)
    else:
        return filter_sensitive(arr,
                                absolute_sensitivity=absolute_sensitivity,
                                relative_sensitivity=relative_sensitivity,
                                getter=getter)


def get_all_zigzag(arr, getter):
    '''Get all highs and lows

    Get all highs and lows. The resulting array is guaranteed to alternate
    between highs and lows.
    '''
    if len(arr) <= 1:
        # return a copy of the list
        return arr[:]

    last = arr[0]
    result = [last]

    for i in range(1, len(arr) - 1):
        # figure out whether to keep y
        x = getter(last)
        y = getter(arr[i])
        z = getter(arr[i + 1])
        if x <= y <= z or x >= y >= z:
            # nothing happens
            pass
        else:
            last = arr[i]
            result.append(last)

    result.append(arr[-1])
    return result


def filter_sensitive(arr,
                     absolute_sensitivity=None,
                     relative_sensitivity=None,
                     getter=lambda x: x):
    '''Return highs and lows, filtered by sensitivity.

    Given an array, this function returns an array that is guaranteed to
    alternate between highs and lows. Additionally, variations smaller than
    `sensitivity` are removed.
    '''
    result = get_all_zigzag(arr, getter=getter)

    length = len(result)

    def absolute_meets_threshold(b, c):
        return abs(c - b) >= absolute_sensitivity

    def relative_meets_threshold(b, c):
        assert relative_sensitivity >= 1

        if b < c:
            diff = c / float(b)
        else:
            diff = b / float(c)

        return diff >= relative_sensitivity

    if absolute_sensitivity:
        meets_threshold = absolute_meets_threshold
    else:
        meets_threshold = relative_meets_threshold

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

        if middle_points and not meets_threshold(b, c):
            # remove
            del result[i + 1:i + 3]
            i -= 2
        else:
            i -= 1

    return result


# execute the whole thing!
if __name__ == '__main__':
    main()
