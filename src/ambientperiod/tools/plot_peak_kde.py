import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.stats import gaussian_kde, entropy

def plot_peak_kde(mfx, mfs, vent, fs, bins=30):
    """
    KDE plot of dominant frequencies (log-scale x-axis) with entropy annotation.
    """
    freqs = mfx[:, 0]

    dom_freqs = []
    nwin = mfs.shape[1]
    for i in range(nwin):
        spec = mfs[:, i]
        peaks, _ = find_peaks(spec)
        if len(peaks) > 0:
            pi = peaks[np.argmax(spec[peaks])]
            fdom = freqs[pi]
            if np.isfinite(fdom):
                dom_freqs.append(fdom)

    # Convert to numpy and remove NaN/infs just in case
    dom = np.array(dom_freqs)
    dom = dom[np.isfinite(dom)]

    print(f"[INFO] Dominant frequencies count: {len(dom)}")
    print(f"[INFO] Any NaN? {np.isnan(dom).any()}, Any Inf? {np.isinf(dom).any()}")

    if len(dom) < 5:
        print("⚠️ Not enough valid dominant frequencies to perform KDE.")
        return

    try:
        kde = gaussian_kde(dom)
    except Exception as e:
        print(f"❌ KDE failed: {e}")
        return

    xs = np.logspace(np.log10(freqs.min()), np.log10(freqs.max()), 300)
    kde_vals = kde(xs)

    mode_idx = np.argmax(kde_vals)
    f_mode = xs[mode_idx]

    # Histogram entropy
    counts, _ = np.histogram(dom, bins=bins, density=True)
    prob = counts / counts.sum()
    H = entropy(prob[prob > 0], base=2)

    # Plot
    plt.figure(figsize=(10, 5))
    plt.semilogx(xs, kde_vals, color='darkblue', lw=2, label="KDE")
    plt.axvline(f_mode, color='red', linestyle='--', lw=1.5, label=f"Mode = {f_mode:.2f} Hz")
    plt.xlabel("Frequency [Hz] (log scale)", fontweight='bold')
    plt.ylabel("Density", fontweight='bold')
    plt.title(f"Dominant Frequency KDE  •  Entropy = {H:.2f} bits", fontweight='bold')
    plt.legend()
    plt.grid(True, which='both', ls='--', lw=0.5, alpha=0.6)
    plt.tight_layout()
    plt.show()
