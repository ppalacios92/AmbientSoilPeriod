import numpy as np

def prom_vent(mfs):
    m, n = mfs.shape
    s = np.sum(mfs, axis=1)
    mfp = s / n
    return mfp
