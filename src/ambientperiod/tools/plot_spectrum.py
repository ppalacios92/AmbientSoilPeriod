import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def plot_spectrum(mfx, mfs, mfp, peak_spacing_hz=0.5):

    df = mfx[1, 0] - mfx[0, 0]
    peak_spacing_samples = int(peak_spacing_hz / df)

    plt.figure(figsize=(10, 6), facecolor='white')

    # Subplot 1 — All spectra
    plt.subplot(2, 1, 1)
    plt.semilogx(mfx, mfs, alpha=0.6)
    plt.grid(True, which='both', axis='both')
    plt.xlabel('Frequency [Hz]', fontsize=10, fontweight='bold')
    plt.ylabel('Amplitude', fontsize=10, fontweight='bold')
    plt.title('Spectrum', fontsize=11, fontweight='bold')

    # Subplot 2 — Average spectrum and peaks
    plt.subplot(2, 1, 2)
    plt.semilogx(mfx[:, 0], mfp, linewidth=2)
    plt.grid(True, which='both', axis='both')
    plt.xlabel('Frequency [Hz]', fontsize=10, fontweight='bold')
    plt.ylabel('Amplitude', fontsize=10, fontweight='bold')
    plt.title('Average Spectrum', fontsize=11, fontweight='bold')

    peaks, _ = find_peaks(mfp, distance=peak_spacing_samples)
    sorted_peaks = peaks[np.argsort(mfp[peaks])[::-1]]
    top_peaks = sorted_peaks[:4]

    for idx in top_peaks:
        f = mfx[idx, 0]
        T = 1.0 / f if f != 0 else 0.0
        label = f'← f={f:.2f} Hz / T={T:.2f} s'
        plt.text(f, mfp[idx], label, fontsize=8)

    plt.legend(['Average Spectrum'], loc='lower center')
    plt.box(True)
    plt.tight_layout()
    plt.show()
