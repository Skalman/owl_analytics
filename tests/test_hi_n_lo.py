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

import unittest
import hi_n_lo


class TestHi_n_lo(unittest.TestCase):
	""" Test class for function get_hi_n_lo.
	"""


	def run_tuples(self, message, data, sensitivity = 2, getter = lambda x: x[1]):
		""" (TestHi_n_lo, list of tuple, string)

		Takes a list of data points `data`, and calls `get_hi_n_lo()`. Asserts that
		the resulting data points match those expected.

		* `data` - A list of data points. Each data point is a tuple, where the
		  second item is the number which will be considered in the filtering.
		  If the tuple in question is expected in the output, the third item must be
		  the string 'expected'.
		"""
		actual = hi_n_lo.get_hi_n_lo(data, sensitivity, getter)

		# filter out the expected results
		expected = [item for item in data if item[-1] == 'expected']

		self.assertEqual(expected, actual, message)


	def test_empty(self):
		self.run_tuples('Empty dataset', [])


	def test_rand0(self):
		self.run_tuples('Dataset "Rand0"', [
				(1,  3, 'expected'),
				(2,  2),
				(3,  1, 'expected'),
				(4,  3),
				(5,  3),
				(6,  2),
				(7,  5, 'expected'),
				(8,  3),
				(9,  2, 'expected'),
				(10, 3),
				(11, 4, 'expected'),
			])

	def test_rand1(self):
		self.run_tuples('Dataset "Rand1"', [
			(1, 4, 'expected'),
			(2, 3, 'expected'),
			(3, 4),
			(4, 5),
			(5, 6, 'expected'),
			(6, 1, 'expected'),
		])

	def test_rand2(self):
		self.run_tuples('Dataset "Rand2"', [
			(1, 9, 'expected'),
			(2, 7),
			(3, 6),
			(4, 2, 'expected'),
			(5, 3),
			(6, 8, 'expected'),
			(7, 1, 'expected'),
			(8, 2),
			(9, 4, 'expected'),
		])

	
	def test_r0_f0(self):
		self.run_tuples('Dataset "R0 / F0"', [
			(1, 3, 'expected'),
		])

	def test_r1(self):
		self.run_tuples('Dataset "R1"', [
			(1, 1, 'expected'),
			(2, 2),
			(3, 3),
			(4, 4),
			(5, 5),
			(6, 6, 'expected'),
		])

	def test_r2(self):
		self.run_tuples('Dataset "R2"', [
			(1, 2, 'expected'),
			(2, 3, 'expected'),
		])

	def test_r3(self):
		self.run_tuples('Dataset "R3"', [
			(1, 3, 'expected'),
			(2, 6, 'expected'),
			(3, 4, 'expected'),
		])

	def test_r4(self):
		self.run_tuples('Dataset "R4"', [
			(1, 6, 'expected'),
			(2, 3, 'expected'),
			(3, 6, 'expected'),
		])

	def test_r5(self):
		self.run_tuples('Dataset "R5"', [
			(1, 3, 'expected'),
			(2, 6, 'expected'),
			(3, 5, 'expected'),
		])

	def test_r6(self):
		self.run_tuples('Dataset "R6"', [
			(1, 3, 'expected'),
			(2, 2, 'expected'),
			(3, 6, 'expected'),
		])

	def test_f1(self):
		self.run_tuples('Dataset "F1"', [
			(1, 3, 'expected'),
			(2, 2, 'expected'),
		])

	def test_f2(self):
		self.run_tuples('Dataset "F2"', [
			(1, 3, 'expected'),
			(2, 6, 'expected'),
			(3, 2, 'expected'),
		])

	def test_f3(self):
		self.run_tuples('Dataset "F3"', [
			(1, 3, 'expected'),
			(2, 6, 'expected'),
			(3, 4),
			(4, 2, 'expected'),
		])

	def test_f4(self):
		self.run_tuples('Dataset "F4"', [
			(1, 3, 'expected'),
			(2, 6, 'expected'),
			(3, 4),
			(4, 5),
			(5, 2),
			(6, 1, 'expected'),
		])

	def test_f5(self):
		self.run_tuples('Dataset "F5"', [
			(1, 3, 'expected'),
			(2, 6, 'expected'),
			(3, 2),
			(4, 1, 'expected'),
		])

	def test_f6(self):
		self.run_tuples('Dataset "F6"', [
			(1, 6, 'expected'),
			(2, 5),
			(3, 4),
			(4, 3),
			(5, 2),
			(6, 1, 'expected'),
		])

	def test_f7(self):
		self.run_tuples('Dataset "F7"', [
			(1, 3, 'expected'),
			(2, 6, 'expected'),
			(3, 3, 'expected'),
		])


if __name__ == '__main__':
	unittest.main(exit=False)
