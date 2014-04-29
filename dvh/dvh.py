#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

def monotonic_increasing(list_):
    """Check if input list is monotonically increasing"""
    return np.all(np.diff(list_) >= 0)


def monotonic_decreasing(list_):
    """Check if input list is monotonically decreasing"""
    return np.all(np.diff(list_) <= 0)

def differential_to_cumulative(doses, volumes):
    cum =np.cumsum(volumes[::-1])[::-1]
    return cum


class DVH(object):

    def __init__(self, doses=None, volumes=None):
        """
        doses, volumes are arrays of equal length representing points on a
        cumulative dose volume histogram curve.
        """

        if doses is None or volumes is None:
            raise ValueError("You must pass both doses and volumes arrays")

        if not monotonic_increasing(doses):
            raise ValueError("Input doses must be montonically increasing")

        if not monotonic_decreasing(volumes):
            volumes = differential_to_cumulative(doses, volumes)

        if len(volumes) != len(doses):
            raise ValueError("Mismatch between length of volumes and dose arrays")


        self.doses = np.array(doses, dtype=np.float)
        self._volumes = np.array(volumes, dtype=np.float)

        # force dose to zero for first point
        if self.doses[0] != 0:
            self.doses = np.insert(self.doses, 0, 0)
            self._volumes = np.insert(self._volumes, 0, self._volumes[0])

        # force volumes to zero for last point
        if self._volumes[-1] != 0:
            self.doses = np.append(self.doses, self.doses[-1] + (self.doses[-1] - self.doses[-2]))
            self._volumes  = np.append(self._volumes, 0)

        self._set_volumes()
        self._calculate_stats()


    def _set_volumes(self):

        self.cum_volumes = self._volumes/self._volumes.max()
        self.diff_volumes = np.append(np.diff(self.cum_volumes[::-1])[::-1], self.cum_volumes[-1])

        # sanity check
        assert len(self.doses) == len(self.diff_volumes) and len(self.diff_volumes) == len(self.cum_volumes)


    def _calculate_stats(self):
        self.mean_dose = (self.doses * self.diff_volumes).sum()
        nonzero = np.where(self.diff_volumes > 0)[0]

        # special case to handle Monaco min dose = 0
        if self.doses[1] == (self.doses[2] - self.doses[1])/2:
            self.min_dose = 0.
        else:
            self.min_dose = self.doses[nonzero[0]]

        self.max_dose = self.doses[nonzero[-1]]

    def dose_to_volume_fraction(self, volume_fraction):
        """Return the dose that receives at least volume_fraction % dose (e.g.
        dvh.dose_to_volume_fraction(0.9) == D90% ).
        Doses are linearly interpreted between two enclosing bin centres.
        """

        if volume_fraction < 0. or volume_fraction > 1.:
            raise ValueError("%.3G is outside expected volume fraction range of 0 <= v <= 1" % (volume_fraction))

        if volume_fraction == 0:
            return self.max_dose
        elif volume_fraction == 1.:
            return self.min_dose

        try:
            lower_idx = np.where(self.cum_volumes >= volume_fraction)[0][-1] #
            l, u = lower_idx, lower_idx+1
            ds, vs = self.doses, self.cum_volumes
            return ds[l] + (ds[u] - ds[l])*(volume_fraction - vs[l]) / (vs[u] - vs[l])
        except IndexError: # pragma:nocover
            # should never hit this since we always stick have a zero volume point on end of dvh
            raise ValueError("DVH is truncated.  Unable to calculate dose to requested volume fraction")

    def volume_fraction_receiving_dose(self, dose):
        """ Return the fraction of total volume recieving at least the input dose. (e.g.
        dvh.volume_fraction_receiving_dose(50) == V50Gy ).

        Volumes are linearly interpreted between two enclosing points.
        """

        if dose > self.max_dose:
            return 0
        elif dose <= self.min_dose:
            return 1.

        lower_idx = np.where(self.doses <= dose)[0][-1]
        l, u = lower_idx, lower_idx + 1
        ds, vs = self.doses, self.cum_volumes

        return vs[l]+(vs[u]-vs[l])*(dose-ds[l])/(ds[u]-ds[l])
