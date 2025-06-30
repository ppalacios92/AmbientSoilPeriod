# Plot STA, LTA, and STA/LTA ratio using plt only

import numpy as np
import matplotlib.pyplot as plt

def plot_sta_lta(signal, sta, lta, ratio, fs, vmin, vmax, vent):
    t = np.arange(len(signal)) / fs

    # Signal
    plt.figure(figsize=(10, 3))
    plt.plot(t, signal)
    plt.title("Signal", fontsize=11, fontweight='bold')
    plt.xlabel("Time [s]", fontsize=9, fontweight='bold')
    plt.ylabel("Signal", fontsize=9, fontweight='bold')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # STA
    plt.figure(figsize=(10, 3))
    plt.plot(t, sta)
    plt.title("Short-Term Average (STA)", fontsize=11, fontweight='bold')
    plt.xlabel("Time [s]", fontsize=9, fontweight='bold')
    plt.ylabel("STA", fontsize=9, fontweight='bold')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # LTA
    plt.figure(figsize=(10, 3))
    plt.plot(t, lta)
    plt.title("Long-Term Average (LTA)", fontsize=11, fontweight='bold')
    plt.xlabel("Time [s]", fontsize=9, fontweight='bold')
    plt.ylabel("LTA", fontsize=9, fontweight='bold')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # STA/LTA Ratio
    plt.figure(figsize=(10, 3))
    plt.plot(t, ratio, label="STA/LTA")
    plt.axhline(vmin, color='red', linestyle='--', label=f"vmin = {vmin}")
    plt.axhline(vmax, color='red', linestyle='--', label=f"vmax = {vmax}")

    n_windows = int(np.max(t) // vent)
    for i in range(1, n_windows + 1):
        plt.axvline(i * vent, color='gray', linestyle=':', linewidth=0.5)

    plt.title("STA / LTA Ratio", fontsize=11, fontweight='bold')
    plt.xlabel("Time [s]", fontsize=9, fontweight='bold')
    plt.ylabel("STA / LTA", fontsize=9, fontweight='bold')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
