
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


def plot_peak_histogram(mfx, mfs, peak_spacing_hz=0.2, height=None, bins=20):


    peak_freqs = []

    for j in range(mfs.shape[1]):
        f = mfx[:, j]
        s = mfs[:, j]

        peaks, _ = find_peaks(s, distance=peak_spacing_hz / (f[1] - f[0]), height=height)
        peak_freqs.extend(f[peaks])

    plt.figure(figsize=(10, 4))
    plt.hist(peak_freqs, bins=bins, color='steelblue', edgecolor='black', alpha=0.7)
    plt.title('Histogram of Peak Frequencies', fontweight='bold')
    plt.xlabel('Frequency [Hz]', fontweight='bold')
    plt.ylabel('Count', fontweight='bold')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
