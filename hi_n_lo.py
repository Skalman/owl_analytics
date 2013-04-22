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
# ./hi_n_lo.py -s 0.03 < data/marketdata.csv > data/marketdata-filtered.csv
# ./hi_n_lo.py -s 0.03 -i data/marketdata.csv -o data/marketdata-filtered.csv


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

	parser.add_argument('-s, --sensitivity', metavar='<num>', default=0, type=float,
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
			data.append( (row[0], float(row[1])) )

	# calculate
	hi_n_lo = get_hi_n_lo(data, getter = lambda x: x[1], sensitivity = args.sensitivity)

	# write to file
	csvwriter = csv.writer(output, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	csvwriter.writerow(header)
	csvwriter.writerows(hi_n_lo)


def get_hi_n_lo(arr, sensitivity = 0, getter = lambda x: x ):
	if sensitivity == 0:
		return get_all_hi_n_lo(arr, getter = getter)
	else:
		return filter_sensitive(arr, sensitivity = sensitivity, getter = getter)


def get_all_hi_n_lo(arr, getter):
	"""
	Get all highs and lows. The resulting array is guaranteed to alternate
	between highs and lows.
	"""
	if len(arr) <= 1:
		# return a copy of the list
		return arr[:]

	last = arr[0]
	result = [last]

	for i in range(1, len(arr)-1):
		# figure out whether to keep y
		x = getter(last)
		y = getter(arr[i])
		z = getter(arr[i+1])
		if x <= y <= z or x >= y >= z:
			# nothing happens
			pass
		else:
			last = arr[i]
			result.append(last)

	result.append(arr[-1])
	return result

def filter_sensitive(arr, sensitivity, getter):
	"""
	Given an array, this function returns an array that is guaranteed to
	alternate between highs and lows. Additionally, variations smaller than
	`sensitivity` are removed.
	"""
	result = get_all_hi_n_lo(arr, getter = getter)

	length = len(result)

	i = length - 4
	while i >= 0:
		# Use four points a-b-c-d to figure out whether we can safely remove b and c
		a = getter(result[i])
		b = getter(result[i + 1])
		c = getter(result[i + 2])
		d = getter(result[i + 3])

		remove = False
		if abs(b - c) < sensitivity:
			if b < c:
				# b and d are low points
				remove = a > c and b > d
			else:
				# a and c are low points
				remove = a < c and b < d

		if remove:
			del result[i+1:i+3]
			# TODO figure out whether we should really move two steps back
			i -= 2
		else:
			i -= 1

	return result


# execute the whole thing!
if __name__ == '__main__':
	main()
