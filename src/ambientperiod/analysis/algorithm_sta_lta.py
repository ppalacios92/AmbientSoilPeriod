# Optimized STA/LTA ratio computation using convolution

import numpy as np

def algorithm_sta_lta(signal, fs, sta, lta):
    n_sta = int(fs * sta)
    n_lta = int(fs * lta)

    signal_sq = signal**2

    # Moving average via convolution (same length output)
    sta_kernel = np.ones(n_sta) / n_sta
    lta_kernel = np.ones(n_lta) / n_lta

    sta_vals = np.convolve(signal_sq, sta_kernel, mode='same')
    lta_vals = np.convolve(signal_sq, lta_kernel, mode='same')

    # Avoid division by zero
    lta_vals[lta_vals == 0] = 1e-12

    sta_lta_ratio = sta_vals / lta_vals

    return sta_lta_ratio, sta_vals, lta_vals
