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


class TestMaxPoints(unittest.TestCase):

    '''Test class for function max_points.
    '''

    def run_test(self, message, data, points=4, getter=lambda x: x[1]):
        actual = zigzag.max_points(data,
                                   points=points,
                                   getter=getter)

        # filter out the expected results
        expected = [item for item in data if item[-1] == 'expected']

        self.assertEqual(expected, actual, message)

    def test_flat(self):
        '''
        An empty list is expected.
        '''
        self.run_test(
            'Flat', points=2,
            data=[
                (1, 1),
                (2, 1),
                (3, 1),
                (4, 1),
            ]
        )

    def test_odd(self):
        self.run_test(
            'Minimal odd case', points=2,
            data=[
                (1, 1),
                (2, 7, 'expected'),
                (3, 4),
                (4, 6),
                (5, 5),
            ]
        )
