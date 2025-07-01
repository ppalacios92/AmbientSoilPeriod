import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def plot_spectrum(mfx, mfs, mfp, peak_spacing_hz=0.5, numer_peaks=2,
                  xlim=None, ylim=None):
    """
    Plot all individual spectra and the average spectrum in a single figure,
    with pastel markers for main peaks and formal legend entries.

    Parameters
    ----------
    mfx : np.ndarray
        Frequency vector (1D or 2D column).
    mfs : np.ndarray
        Spectral amplitudes for all windows.
    mfp : np.ndarray
        Mean spectrum.
    peak_spacing_hz : float, optional
        Minimum distance between peaks in Hz.
    numer_peaks : int, optional
        Number of peaks to highlight.
    xlim : list or tuple [xmin, xmax], optional
        Limits for the x-axis (frequency).
    ylim : list or tuple [ymin, ymax], optional
        Limits for the y-axis (amplitude).
    """
    mfx1d = mfx[:, 0] if mfx.ndim == 2 else mfx
    df = mfx1d[1] - mfx1d[0]
    peak_spacing_samples = int(peak_spacing_hz / df)

    plt.figure(figsize=(10, 3), facecolor='white')

    # Plot all window spectra
    if mfx.ndim == 2 and mfs.ndim == 2:
        for i in range(mfs.shape[1]):
            plt.semilogx(mfx1d, mfs[:, i], color='lightgray', alpha=0.4)
    else:
        plt.semilogx(mfx1d, mfs, color='lightgray', alpha=0.4)

    # Plot average spectrum
    avg_line, = plt.semilogx(mfx1d, mfp, color='steelblue', linewidth=2, label='Average Spectrum')

    # Find and mark peaks
    peaks, _ = find_peaks(mfp, distance=peak_spacing_samples)
    sorted_peaks = peaks[np.argsort(mfp[peaks])[::-1]]
    top_peaks = sorted_peaks[:numer_peaks]

    pastel_colors = ['mediumaquamarine', 'lightcoral', 'cornflowerblue', 'plum']
    peak_lines = []

    for i, idx in enumerate(top_peaks):
        f = mfx1d[idx]
        T = 1.0 / f if f != 0 else 0.0
        amp = mfp[idx]
        color = pastel_colors[i % len(pastel_colors)]
        line_peak, = plt.plot(f, amp, marker='o', color=color, markersize=6)
        peak_lines.append((line_peak, f'Peak {i+1}: f = {f:.2f} Hz / T = {T:.2f} s'))

    # Labels and grid
    plt.grid(True, which='both', axis='both', linestyle='--', alpha=0.5)
    plt.xlabel('Frequency [Hz]', fontsize=10, fontweight='bold')
    plt.ylabel('Amplitude', fontsize=10, fontweight='bold')
    plt.title('Spectrum and Average (All Windows)', fontsize=11, fontweight='bold')

    # Axis limits
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)

    # Legend
    handles = [avg_line] + [line for line, _ in peak_lines]
    labels = ['Average Spectrum'] + [label for _, label in peak_lines]
    plt.legend(handles, labels, loc='upper right', fontsize=9)

    plt.tight_layout()
    plt.show()
