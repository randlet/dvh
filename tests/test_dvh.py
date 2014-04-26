#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dvh
----------------------------------

Tests for `dvh` module.
"""

import unittest
import numpy as np
from dvh import DVH, monotonic_increasing, monotonic_decreasing


class TestDvh(unittest.TestCase):

    def setUp(self):

        self.test_diff_vols = [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 4, 2, 1, 0, 0, 0, 0, 0, 10, 20, 30, 40, 50, 60, 70, 60, 50, 40, 30, 20, 10, 0, 0]
        self.test_cum_vols = [ 518,  518,  518,  518,  518,  518,  518,  518,  518,  517,  515,  512,  508,  503,  497,  493,  491,  490,  490,  490,  490,  490,  490,  480,  460,  430,  390,  340,  280,  210,  150,  100,   60,   30,   10,    0,  0.]
        self.min_dose = 85
        self.max_dose = 345
        self.mean_dose = 285
        self.test_doses = np.arange(0, 371, 10)
        self.bin_mids = np.arange(5, 366, 10)

    def test_bin_mids(self):
        dvh = DVH(self.test_doses, self.test_diff_vols)
        self.assertAlmostEqual(sum(dvh.bin_mids - self.bin_mids), 0)

    def test_dmax(self):
        dvh = DVH(self.test_doses, self.test_diff_vols)
        self.assertEqual(dvh.max_dose, self.max_dose)

    def test_dmin(self):
        dvh = DVH(self.test_doses, self.test_diff_vols)
        self.assertEqual(dvh.min_dose, self.min_dose)

    def test_dmean(self):
        """TODO: Develop real worlds tests"""
        doses = [0, 1, 2, 3, 4]
        volumes = [10, 0, 0, 10]

        dvh = DVH(doses, volumes)
        self.assertEqual(dvh.mean_dose, 2)

    def test_unequal_bin_mids(self):
        bins = [0, 10, 40, 100]
        volumes = [1, 2, 3]
        bin_mids = [5, 25, 70]
        dvh = DVH(bins, volumes)
        self.assertAlmostEqual(sum(dvh.bin_mids - bin_mids), 0)

    def test_monotonic_increasing_strict(self):
        self.assertTrue(monotonic_increasing(range(4)))
        self.assertFalse(monotonic_increasing(self.test_diff_vols))

    def test_monotonic_decreasing(self):
        self.assertFalse(monotonic_decreasing(self.test_diff_vols))
        self.assertTrue(monotonic_decreasing(list(reversed(range(4)))))

    def test_diff_converted_to_cumulative(self):
        dvh = DVH(self.test_doses, self.test_diff_vols)
        self.assertAlmostEqual(dvh.cum_volumes[0], 1)

    def test_invalid_bin_count(self):
        with self.assertRaises(ValueError):
            dvh = DVH(self.test_doses[:-1], self.test_diff_vols)

    def test_invalid_bins(self):
        with self.assertRaises(ValueError):
            dvh = DVH([1,3,1], [2,4])

    def test_cumulative_to_diff(self):
        dvh = DVH(self.test_doses, self.test_cum_vols)
        dvh2 = DVH(self.test_doses, dvh.diff_volumes)
        self.assertAlmostEqual(sum(dvh2.cum_volumes - dvh.cum_volumes), 0)

    def test_dose_to_volume_fraction_0(self):
        dvh = DVH(self.test_doses, self.test_cum_vols)
        self.assertAlmostEqual(dvh.dose_to_volume_fraction(0), self.max_dose)

    def test_dose_to_volume_fraction_1(self):
        dvh = DVH(self.test_doses, self.test_cum_vols)
        self.assertAlmostEqual(dvh.dose_to_volume_fraction(1), self.min_dose)

    def test_dose_to_volume_fraction_mid(self):
        dvh = DVH(self.test_doses, self.test_cum_vols)
        self.assertAlmostEqual(dvh.dose_to_volume_fraction(0.5), self.mean_dose)

    def test_dose_to_volume_fraction_invalid(self):
        dvh = DVH(self.test_doses, self.test_cum_vols)
        with self.assertRaises(ValueError):
            dvh.dose_to_volume_fraction(100)

if __name__ == '__main__':
    unittest.main()

    def test_dose_to_volume_fraction_invalid(self):
        dvh = DVH(self.test_doses, self.test_cum_vols)
        with self.assertRaises(ValueError):
            dvh.dose_to_volume_fraction(100)

if __name__ == '__main__':
    unittest.main()
