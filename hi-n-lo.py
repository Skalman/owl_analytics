#! /usr/bin/env python3

# example usage (the two variants will do the exact same thing):
# ./hi-n-lo.py -s 0.03 < data/marketdata.csv > data/marketdata-filtered.csv
# ./hi-n-lo.py -s 0.03 -i data/marketdata.csv -o data/marketdata-filtered.csv

import sys
import csv
import argparse

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
	header = False

	if args.input == None or args.input == '-':
		input = sys.stdin
	else:
		input = open(args.input, 'r')

	if args.output == None or args.output == '-':
		output = sys.stdout
	else:
		output = open(args.output, 'w')

	# read from stdin
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

	# write to stdout
	csvwriter = csv.writer(output, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	csvwriter.writerow(header)
	csvwriter.writerows(hi_n_lo)


def get_hi_n_lo(arr, sensitivity = 0, compare_index = 0):
	result = [ arr[0] ]
	for i in range(1, len(arr)-1):
		x, y, z = arr[i-1][compare_index], arr[i][compare_index], arr[i+1][compare_index]

		if x < y < z or x > y > z or x == y == z:
			# nothing happens
			pass
		elif sensitivity != 0 and y == z:
			# if sensitivity is non-zero, don't allow multiple same-value items
			pass
		else:
			result.append(arr[i])

	result.append(arr[len(arr)-1])
	if 0 < sensitivity:
		filter_sensitive(result, sensitivity = sensitivity, compare_index = compare_index)

	return result


def filter_sensitive(result, sensitivity, compare_index):
	i = len(result)-1
	while i > 0:
		x, y = result[i-1][compare_index], result[i][compare_index]
		if abs(x - y) < sensitivity:
			del result[i-1:i+1]
			# we also deleted the previous
			i -= 1

		i -= 1

	return result


# execute the whole thing!
main()
