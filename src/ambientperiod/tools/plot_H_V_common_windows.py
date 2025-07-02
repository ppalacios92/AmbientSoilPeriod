import numpy as np
from ambientperiod.tools.plot_spectrum import plot_spectrum

def plot_H_V_common_windows(builders, peak_spacing_hz=0.2, numer_peaks=2, min_freq=0.1 , xlim=None, ylim=None):
    """
    Computes and plots Nakamura (H/V) spectra for common windows across multiple builder groups.

    Parameters
    ----------
    builders : list of tuples
        Each tuple contains (builder_X, builder_Y, builder_Z)
    peak_spacing_hz : float
        Minimum spacing in Hz between detected peaks
    numer_peaks : int
        Number of dominant peaks to annotate
    min_freq : float
        Minimum frequency to display
    """
    epsilon = 1e-10
    nakamura_all_windows = []

    # Frecuencia base
    mfx = builders[0][0].mfx
    if mfx.ndim == 2:
        mfx = mfx[:, 0]

    for builder_X, builder_Y, builder_Z in builders:
        common_ids = builder_X.common_win_ids
        mfs_X = builder_X.mfs[:, [np.where(builder_X.win_ids == i)[0][0] for i in common_ids]]
        mfs_Y = builder_Y.mfs[:, [np.where(builder_Y.win_ids == i)[0][0] for i in common_ids]]
        mfs_Z = builder_Z.mfs[:, [np.where(builder_Z.win_ids == i)[0][0] for i in common_ids]]

        for i in range(len(common_ids)):
            h1 = mfs_X[:, i]
            h2 = mfs_Y[:, i]
            v  = mfs_Z[:, i]
            nakamura = np.sqrt((h1**2 + h2**2) ) / (v + epsilon)
            nakamura_all_windows.append(nakamura)

    nakamura_all_windows = np.column_stack(nakamura_all_windows)
    nakamura_mean = np.mean(nakamura_all_windows, axis=1)

    print("Plot Nakamura (H/V)")
    plot_spectrum(mfx, nakamura_all_windows, nakamura_mean,
                  peak_spacing_hz=peak_spacing_hz,
                  numer_peaks=numer_peaks,
                  min_freq=min_freq , xlim=xlim, ylim=ylim)
