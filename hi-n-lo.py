#! /usr/bin/env python3

# example usage:
# ./hi-n-lo.py < data/marketdata.csv > data/marketdata-filtered.csv

import sys
import csv

def main():
	data = []
	header = False

	# read from stdin
	csvreader = csv.reader(sys.stdin, delimiter=',', quotechar='|')

	is_first = True
	for row in csvreader:
		if is_first:
			# the first row contains the header
			header = row
			is_first = False
		else:
			data.append( (row[0], float(row[1])) )

	# calculate
	hi_n_lo = get_hi_n_lo(data, compare_index = 1, sensitivity = 0.03)

	# write to stdout
	csvwriter = csv.writer(sys.stdout, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
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
