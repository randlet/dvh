#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

def monotonic_increasing(list_):
    """Check if input list is monotonically increasing"""
    return np.all(np.diff(list_) >= 0)


def monotonic_decreasing(list_):
    """Check if input list is monotonically decreasing"""
    return np.all(np.diff(list_) <= 0)


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

        if not monotonic_increasing(self.bins):
            raise ValueError("Input doses must be montonically increasing")

        self._volumes = np.array(volumes, dtype=np.float)
        self._norm_volumes = self._volumes/self._volumes.sum()

        dvh_is_cumulative = monotonic_decreasing(self._volumes) and (self._norm_volumes[0] == 1.)

        if dvh_is_cumulative:
           self.cum_volumes = self._norm_volumes
           self.diff_volumes = np.diff(self.
        else:
            self.cum_volumes = np.cumsum(self._volumes[::-1])[::-1]
            self.diff_volumes = self._norm_volumes

        if len(self.bins) != len(self.diff_volumes) + 1 or len(self.diff_volumes) != len(self.cum_volumes):
            raise ValueError(
                "Invalid number of bins. bins should be a list of bin "
                "edges including the right most edge. len(bins) must be "
                "equal to len(volumes) + 1"
            )



