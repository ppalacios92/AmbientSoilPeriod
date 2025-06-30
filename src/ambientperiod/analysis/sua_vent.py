from numba import njit
import numpy as np

@njit
def sua_vent(mfx, mfz, bexp):
    """
    Smooth the vertical spectrum mfz with Konno-Ohmachi style smoothing
    using a manually implemented kernel (Numba-accelerated).

    Parameters
    ----------
    mfx : ndarray (n_frequencies, n_windows)
        Frequency values per window.
    mfz : ndarray (n_frequencies, n_windows)
        Spectrum values per window (e.g., Z-component).
    bexp : float
        Bandwidth exponent for smoothing.

    Returns
    -------
    mfs : ndarray
        Smoothed spectrum of same shape as mfz.
    """
    mm, nn = mfz.shape
    mfs = np.zeros_like(mfz)

    for j in range(nn):
        y = mfz[:, j]
        f = mfx[:, j]
        nx = len(f)
        dx = f[1] - f[0]
        fratio = 10 ** (2.5 / bexp)

        for ix in range(nx):
            fc = f[ix]
            if fc <= 0:
                continue  # skip invalid frequency

            ix1 = max(int(fc / fratio / dx), 1)
            ix2 = min(int(fc * fratio / dx + 1), nx - 1)

            a1 = 0.0
            a2 = 0.0

            for jx in range(ix1, ix2 + 1):
                if jx != ix and f[jx] > 0:
                    log_ratio = np.log10(f[jx] / fc)
                    d = log_ratio * bexp
                    if d != 0.0:
                        s = np.sin(d)
                        c = (s / d) ** 4
                    else:
                        c = 1.0
                else:
                    c = 1.0
                a1 += c * y[jx]
                a2 += c

            mfs[ix, j] = a1 / a2 if a2 != 0 else 0.0

    return mfs
