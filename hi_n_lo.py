#! /usr/bin/env python3

# example usage (the two variants will do the exact same thing):
# ./hi-n-lo.py -s 0.03 < data/marketdata.csv > data/marketdata-filtered.csv
# ./hi-n-lo.py -s 0.03 -i data/marketdata.csv -o data/marketdata-filtered.csv

import sys
import csv
import argparse


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


def main():
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
	hi_n_lo = get_hi_n_lo(data, compare_index = 1, sensitivity = args.sensitivity)

	# write to file
	csvwriter = csv.writer(output, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	csvwriter.writerow(header)
	csvwriter.writerows(hi_n_lo)


def get_hi_n_lo(arr, sensitivity = 0, compare_index = 0):
	if sensitivity == 0:
		return get_all_hi_n_lo(arr, compare_index = compare_index)
	else:
		return filter_sensitive(arr, sensitivity = sensitivity, compare_index = compare_index)


def get_all_hi_n_lo(arr, compare_index):
	"""
	Get all highs and lows. The resulting array is guaranteed to alternate
	between highs and lows.
	"""
	last = arr[0]
	result = [last]

	for i in range(1, len(arr)-1):
		# figure out whether to keep y
		x = last[compare_index]
		y = arr[i][compare_index]
		z = arr[i+1][compare_index]
		if x <= y <= z or x >= y >= z:
			# nothing happens
			pass
		else:
			last = arr[i]
			result.append(last)

	result.append(arr[-1])
	return result

def filter_sensitive(arr, sensitivity, compare_index):
	"""
	Given an array, this function returns an array that is guaranteed to
	alternate between highs and lows. Additionally, variations smaller than
	`sensitivity` are removed.
	"""
	result = get_all_hi_n_lo(arr, compare_index = compare_index)

	length = len(result)

	i = length - 4
	while i >= 0:
		# Use four points a-b-c-d to figure out whether we can safely remove b and c
		a = result[i][compare_index]
		b = result[i + 1][compare_index]
		c = result[i + 2][compare_index]
		d = result[i + 3][compare_index]

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
main()
