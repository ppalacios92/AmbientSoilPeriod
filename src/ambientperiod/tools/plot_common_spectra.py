import numpy as np
from ambientperiod.tools.plot_spectrum import plot_spectrum

def plot_common_spectra(builders):
    """
    Plot the component spectra (X, Y, Z) using only the common window IDs across all builders.

    Parameters
    ----------
    builders : list of tuple
        Each tuple must be (builder_X, builder_Y, builder_Z) and each builder must have:
        - win_ids: array of window IDs
        - mfs: 2D array of spectra (n_frequencies, n_windows)
        - mfx: frequency vector (or 2D with single column)
    """
    labels = ['X', 'Y', 'Z']

    for group in builders:
        # Obtener ids comunes entre los 3 builders
        win_ids = [np.array(b.win_ids) for b in group]
        common_ids = win_ids[0]
        for w in win_ids[1:]:
            common_ids = np.intersect1d(common_ids, w)

        # Determinar cantidad máxima de columnas válidas
        max_cols = min(b.mfs.shape[1] for b in group)
        common_ids = [i for i in common_ids if i < max_cols]

        # Extraer vector de frecuencia
        f = group[0].mfx[:, 0] if group[0].mfx.ndim == 2 else group[0].mfx

        # Graficar cada componente
        for b, label in zip(group, labels):
            mfs = b.mfs[:, common_ids]
            mfs_mean = np.mean(mfs, axis=1)
            print(f"Plot {label}")
            plot_spectrum(
                f, 
                mfs, 
                mfs_mean, 
                peak_spacing_hz=0.2, 
                numer_peaks=3, 
                min_freq=0.2
            )
