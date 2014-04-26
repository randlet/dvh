#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dvh
----------------------------------

Tests for `dvh` module.
"""

import unittest

from dvh import DVH, monotonic_increasing, monotonic_decreasing


class TestDvh(unittest.TestCase):

    def setUp(self):

        self.test_diff_vols = [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 4, 2, 1, 0, 0, 0, 0, 0, 10, 20, 30, 40, 50, 60, 70, 60, 50, 40, 30, 20, 10, 0, 0]

        self.test_cum_vols = [ 518,  518,  518,  518,  518,  518,  518,  518,  518,  517,  515,  512,  508,  503,  497,  493,  491,  490,  490,  490,  490,  490,  490,  480,  460,  430,  390,  340,  280,  210,  150,  100,   60,   30,   10,    0,  0.]
        self.test_doses = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370]

    def test_monotonic_increasing_strict(self):
        self.assertTrue(monotonic_increasing(range(4)))
        self.assertFalse(monotonic_increasing(self.test_diff_vols))

    def test_monotonic_decreasing(self):
        self.assertFalse(monotonic_decreasing(self.test_diff_vols))
        self.assertTrue(monotonic_decreasing(list(reversed(range(4)))))

    def test_diff_converted_to_cumulative(self):
        dvh = DVH(self.test_doses, self.test_diff_vols)
        self.assertAlmostEqual(dvh.cum_volumes[0], 1)

    def test_invalid_bins(self):
        with self.assertRaises(ValueError):
            dvh = DVH(self.test_doses[:-1], self.test_diff_vols)


if __name__ == '__main__':
    unittest.main()
