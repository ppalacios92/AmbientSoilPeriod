# Load signal from file

import numpy as np

def load_utils(path):
    data = np.loadtxt(path)
    if data.ndim > 1 and data.shape[1] == 1:
        data = data[:, 0]
    if data.ndim != 1:
        raise ValueError("Signal must be one-dimensional")
    return data
