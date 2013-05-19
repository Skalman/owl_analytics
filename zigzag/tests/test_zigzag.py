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
import zigzag


class TestZigzag(unittest.TestCase):

    '''Test class for function get_zigzag.
    '''

    def run_absolute_sensitivity(self, message, data, absolute_sensitivity=2, getter=lambda x: x[1]):
        '''(TestZigzag, string, list of tuple)

        Takes a list of data points `data`, and calls `get_zigzag()`. Asserts that
        the resulting data points match those expected.

        * `data` - A list of data points. Each data point is a tuple, where the
          second item is the number which will be considered in the filtering.
          If the tuple in question is expected in the output, the third item must be
          the string 'expected'.
        '''
        actual = zigzag.get_zigzag(data,
                                   absolute_sensitivity=absolute_sensitivity,
                                   getter=getter)

        # filter out the expected results
        expected = [item for item in data if item[-1] == 'expected']

        self.assertEqual(expected, actual, message)

    def test_empty(self):
        self.run_absolute_sensitivity('Empty dataset', [])

    def test_rand0(self):
        self.run_absolute_sensitivity('Dataset "Rand0"', [
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
        self.run_absolute_sensitivity('Dataset "Rand1"', [
            (1, 4, 'expected'),
            (2, 3, 'expected'),
            (3, 4),
            (4, 5),
            (5, 6, 'expected'),
            (6, 1, 'expected'),
        ])

    def test_rand2(self):
        self.run_absolute_sensitivity('Dataset "Rand2"', [
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
        self.run_absolute_sensitivity('Dataset "R0 / F0"', [
            (1, 3, 'expected'),
        ])

    def test_r1(self):
        self.run_absolute_sensitivity('Dataset "R1"', [
            (1, 1, 'expected'),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6, 'expected'),
        ])

    def test_r2(self):
        self.run_absolute_sensitivity('Dataset "R2"', [
            (1, 2, 'expected'),
            (2, 3, 'expected'),
        ])

    def test_r3(self):
        self.run_absolute_sensitivity('Dataset "R3"', [
            (1, 3, 'expected'),
            (2, 6, 'expected'),
            (3, 4, 'expected'),
        ])

    def test_r4(self):
        self.run_absolute_sensitivity('Dataset "R4"', [
            (1, 6, 'expected'),
            (2, 3, 'expected'),
            (3, 6, 'expected'),
        ])

    def test_r5(self):
        self.run_absolute_sensitivity('Dataset "R5"', [
            (1, 3, 'expected'),
            (2, 6, 'expected'),
            (3, 5, 'expected'),
        ])

    def test_r6(self):
        self.run_absolute_sensitivity('Dataset "R6"', [
            (1, 3, 'expected'),
            (2, 2, 'expected'),
            (3, 6, 'expected'),
        ])

    def test_f1(self):
        self.run_absolute_sensitivity('Dataset "F1"', [
            (1, 3, 'expected'),
            (2, 2, 'expected'),
        ])

    def test_f2(self):
        self.run_absolute_sensitivity('Dataset "F2"', [
            (1, 3, 'expected'),
            (2, 6, 'expected'),
            (3, 2, 'expected'),
        ])

    def test_f3(self):
        self.run_absolute_sensitivity('Dataset "F3"', [
            (1, 3, 'expected'),
            (2, 6, 'expected'),
            (3, 4),
            (4, 2, 'expected'),
        ])

    def test_f4(self):
        self.run_absolute_sensitivity('Dataset "F4"', [
            (1, 3, 'expected'),
            (2, 6, 'expected'),
            (3, 4),
            (4, 5),
            (5, 2),
            (6, 1, 'expected'),
        ])

    def test_f5(self):
        self.run_absolute_sensitivity('Dataset "F5"', [
            (1, 3, 'expected'),
            (2, 6, 'expected'),
            (3, 2),
            (4, 1, 'expected'),
        ])

    def test_f6(self):
        self.run_absolute_sensitivity('Dataset "F6"', [
            (1, 6, 'expected'),
            (2, 5),
            (3, 4),
            (4, 3),
            (5, 2),
            (6, 1, 'expected'),
        ])

    def test_f7(self):
        self.run_absolute_sensitivity('Dataset "F7"', [
            (1, 3, 'expected'),
            (2, 6, 'expected'),
            (3, 3, 'expected'),
        ])

    def run_relative_sensitivity(self, message, data, relative_sensitivity=2.5,
                                 getter=lambda x: x[1]):
        '''(TestZigzag, string, list of tuple)

        Takes a list of relative changes to data points `data_changes`, performs
        the transformations and calls `get_zigzag()`. Asserts that the resulting
        data points match those expected.

        * `data` - A list of data points. Each data point is a tuple, where the
          second item is the number which will be considered in the filtering.
          If the tuple in question is expected in the output, the third item
          must be the string 'expected'.
        '''
        actual = zigzag.get_zigzag(data,
                                   relative_sensitivity=relative_sensitivity,
                                   getter=getter)

        # filter out the expected results
        expected = [item for item in data if item[-1] == 'expected']

        self.assertEqual(expected, actual, message)

    def test_relative_rise(self):
        self.run_relative_sensitivity(
            'Relative rise', relative_sensitivity=2.5,
            data=[
                (1, 2, 'expected'),
                (2, 4),
                (3, 2),
                (4, 5, 'expected'),
            ])

    def test_relative_decline(self):
        self.run_relative_sensitivity(
            'Relative decline', relative_sensitivity=2.5,
            data=[
                (1, 10, 'expected'),
                (2, 4),
                (3, 8),
                (4, 4, 'expected'),
            ])

    def test_relative(self):
        self.run_relative_sensitivity(
            'Relative', relative_sensitivity=2,
            data=[
                (1,  3, 'expected'),
                (2,  4),
                (3,  6),
                (4,  4),
                (5,  8, 'expected'),
                (6,  4, 'expected'),
                (7,  8, 'expected'),
                (8,  4, 'expected'),
                (9,  9, 'expected'),
                (10, 5),
                (11, 6),
                (12, 3, 'expected'),
                (13, 5),
                (14, 4),
                (15, 7, 'expected'),
                (16, 1, 'expected'),
                (17, 2, 'expected'),
                (18, 1.5, 'expected'),
            ])


if __name__ == '__main__':
    unittest.main(exit=False)
