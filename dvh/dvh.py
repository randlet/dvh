#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

def monotonic_increasing(list_):
    """Check if input list is monotonically increasing"""
    return np.all(np.diff(list_) >= 0)


def monotonic_decreasing(list_):
    """Check if input list is monotonically decreasing"""
    return np.all(np.diff(list_) <= 0)


#TODO: implement some sort of interpolation scheme rather than just
#TODO: using bin mid points

class DVH(object):

    def __init__(self, bins, volumes):
        """
        bins is a sequence of dose bin edges including the rightmost edge (same
        as numpy.histogram).
        volumes is either differential or cumulative volume corresponding to
        each bin.

        The length of bins must be exactly 1 more than volumes.

        For example:
            bins =    [0, 10, 20, 30, 40]
            volumes = [ 0,  0.5, 0.4, 0.1]
        would mean 50% of volume receives a dose between 10 and 20cGy

        """

        self.bins = np.array(bins, dtype=np.float)
        if self.bins[0] != 0:
            np.insert(self.bins, 0, 0)

        self.bin_mids = self.bins[:-1] + np.diff(self.bins)/2.

        if not monotonic_increasing(self.bins):
            raise ValueError("Input doses must be montonically increasing")

        self._volumes = np.array(volumes, dtype=np.float)

        self._set_volumes()
        self._calculate_stats()


    def _set_volumes(self):

        dvh_is_cumulative = monotonic_decreasing(self._volumes) and (self._volumes[0] == self._volumes.max())

        if dvh_is_cumulative:
            self.cum_volumes = self._volumes/self._volumes.max()
            self.diff_volumes = np.append(np.diff(self.cum_volumes[::-1])[::-1], self.cum_volumes[-1])
        else:
            self.diff_volumes = self._volumes/self._volumes.sum()
            self.cum_volumes = np.cumsum(self.diff_volumes[::-1])[::-1]

        if len(self.bins) != len(self.diff_volumes) + 1 or len(self.diff_volumes) != len(self.cum_volumes):
            raise ValueError(
                "Invalid number of bins. bins should be a list of bin "
                "edges including the right most edge. len(bins) must be "
                "equal to len(volumes) + 1"
            )

    def _calculate_stats(self):
        self.mean_dose = (self.bin_mids*self.diff_volumes).sum()
        nonzero = np.where(self.diff_volumes > 0)[0]
        self.min_dose = self.bin_mids[nonzero[0]]
        self.max_dose = self.bin_mids[nonzero[-1]]

    def dose_to_volume_fraction(self, volume_fraction):
        """return the dose that receives at least volume_fraction % dose"""

        if volume_fraction < 0. or volume_fraction > 1.:
            raise ValueError("%.3G is outside expected volume fraction range of 0 <= v <= 1" % (volume_fraction))

        if volume_fraction == 0:
            return self.max_dose
        elif volume_fraction == 1.:
            return self.min_dose

        idx = np.where(self.cum_volumes>=volume_fraction)[0][-1]

        return self.bin_mids[idx]

    def volume_fraction_receiving_dose(self, dose):
        """return the fraction of total volume recieving the input dose"""

        if dose > self.max_dose:
            return 0
        elif dose <= self.min_dose:
            return 1.

        idx = numpy.where(self.bins<=dose)[0][-1]
        return self.cum_volumes[idx]
