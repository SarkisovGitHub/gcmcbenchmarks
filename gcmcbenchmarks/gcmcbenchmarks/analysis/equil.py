"""Functions for finding equilibrium in gcmc timeseries

"""
import numpy as np


def split_around(sig, thresh):
    """Split *sig* around the first occurence of *thresh*

    Works on rising signals
    """
    
    split = sig[sig > thresh].index[0]
    
    return sig[:split].iloc[:-1], sig[split:]

def check_flat(sig, max_drift=5):
    """Check a portion of signal is flat, else raise error

    Flat defined as not drifting more than 5% of mean
    """
    x0, c = np.polyfit(sig.index, sig.values, 1)

    y0 = c + x0 * sig.index[0]
    y1 = c + x0 * sig.index[-1]

    totdrift = 100 * abs((y1 - y0) / sig.mean())

    # if x0 is very small, dont calculate drift and assume flat
    # fixes issue with very long time series
    if (x0 > 1e-4) and (totdrift > max_drift):
        raise ValueError("Signal drifted {}%."
                         "x0: {} c: {}"
                         "y0: {} y1: {}"
                         "mean: {}".format(
                             totdrift,
                             x0, c,
                             y0, y1,
                             sig.mean))
    else:
        return True

def find_equil(sig, wsize=None):
    """Find number of MC steps to equilibrium

    Parameters
    ----------
    sig : pd.Series
      gcmc timeseries
    wsize : int, optional
      number of MC steps to consider as window for rolling mean
      by default considers 1% of the signal
    """
    if wsize is None:
        # default, consider 1% of signal
        wsize = len(sig) // 100
    else:
        wsize = len(sig[:wsize])

    half = len(sig) // 2
    
    back = sig.iloc[half:]

    check_flat(back)

    mean = back.mean()
    std = back.std()
    thresh = mean - 2 * std
    
    rm = sig.rolling(wsize, center=True).mean()
    
    equil, sampling = split_around(rm, thresh)
    
    return sampling.index[0]
