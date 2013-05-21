#! /usr/bin/env python

# Example usage
# -------------
# The two variants will do the exact same thing:
# ./zigzag_cli.py -s 0.03 < data/marketdata.csv > data/marketdata-filtered.csv
# ./zigzag_cli.py -s 0.03 -i data/marketdata.csv -o data/marketdata-filtered.csv


import sys
import csv
import argparse
import zigzag


def main():
    # argument parsing
    parser = argparse.ArgumentParser(description='find hi and lo values')
    parser.add_argument(
        '-i, --input-file', metavar='<file>', type=str,
        dest='input',
        help='input file (default: stdin)')

    parser.add_argument(
        '-o, --output-file', metavar='<file>', type=str,
        dest='output',
        help='output file (default: stdout)')

    parser.add_argument(
        '-c, --change', metavar='<num>', default=0, type=float,
        dest='change',
        help='change, a percentage between 0 and 100 a non-negative number (default: 0)')

    parser.add_argument(
        '-t, --type', metavar='percent | absolute', type=str,
        dest='type',
        help="type, either 'percent' or 'absolute' (default: percent)")

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
    filtered = zigzag.min_change(data, getter=lambda x: x[1],
                                 change=args.change)

    # write to file
    csvwriter = csv.writer(
        output, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(header)
    csvwriter.writerows(filtered)

if __name__ == '__main__':
    main()
