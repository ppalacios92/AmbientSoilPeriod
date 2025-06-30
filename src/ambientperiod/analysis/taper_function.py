
import numpy as np
from scipy.signal.windows import tukey

def taper_function(MV, p):
    m, _ = MV.shape
    u = tukey(m, alpha=p)
    MA = MV * u[:, np.newaxis]
    return MA, u
