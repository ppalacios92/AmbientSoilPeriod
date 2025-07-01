import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def plot_spectrum(mfx, mfs, mfp, peak_spacing_hz=0.5):
    """
    Grafica todos los espectros individuales y su promedio, 
    con anotación automática de los picos principales.
    """
    # Forzar mfx a forma 1D si es columna
    mfx1d = mfx[:, 0] if mfx.ndim == 2 else mfx
    df = mfx1d[1] - mfx1d[0]
    peak_spacing_samples = int(peak_spacing_hz / df)

    plt.figure(figsize=(10, 6), facecolor='white')

    # Subplot 1 — Todos los espectros
    plt.subplot(2, 1, 1)
    if mfx.ndim == 2 and mfs.ndim == 2:
        for i in range(mfs.shape[1]):
            plt.semilogx(mfx1d, mfs[:, i], alpha=0.3)
    else:
        plt.semilogx(mfx1d, mfs, alpha=0.6)
    plt.grid(True, which='both', axis='both')
    plt.xlabel('Frequency [Hz]', fontsize=10, fontweight='bold')
    plt.ylabel('Amplitude', fontsize=10, fontweight='bold')
    plt.title('Spectrum', fontsize=11, fontweight='bold')

    # Subplot 2 — Espectro promedio con picos
    plt.subplot(2, 1, 2)
    plt.semilogx(mfx1d, mfp, linewidth=2)
    plt.grid(True, which='both', axis='both')
    plt.xlabel('Frequency [Hz]', fontsize=10, fontweight='bold')
    plt.ylabel('Amplitude', fontsize=10, fontweight='bold')
    plt.title('Average Spectrum', fontsize=11, fontweight='bold')

    peaks, _ = find_peaks(mfp, distance=peak_spacing_samples)
    sorted_peaks = peaks[np.argsort(mfp[peaks])[::-1]]
    top_peaks = sorted_peaks[:4]

    for idx in top_peaks:
        f = mfx1d[idx]
        T = 1.0 / f if f != 0 else 0.0
        label = f'← f={f:.2f} Hz / T={T:.2f} s'
        plt.text(f, mfp[idx], label, fontsize=8)

    plt.legend(['Average Spectrum'], loc='lower center')
    plt.box(True)
    plt.tight_layout()
    plt.show()
