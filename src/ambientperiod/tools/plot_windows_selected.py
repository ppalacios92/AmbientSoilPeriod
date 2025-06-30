# Plot selected windows over the signal

import numpy as np
import matplotlib.pyplot as plt

def plot_windows_selected(signal, windows_time, windows_signal, fs):
    t = np.arange(len(signal)) / fs
    
    plt.figure(figsize=(10, 4))
    plt.plot(t, signal, color='black')
    if windows_time.shape[1] > 0:
        min_val = np.min(signal)
        max_val = np.max(signal)
        n_windows = windows_time.shape[1]

        colors = plt.cm.hsv(np.linspace(0, 1, n_windows))

        for i in range(n_windows):
            x0 = windows_time[0, i]
            x1 = windows_time[-1, i]
            y0 = min_val
            y1 = max_val

            x = [x0, x1, x1, x0]
            y = [y0, y0, y1, y1]
            plt.fill(x, y, color=colors[i], alpha=0.35, edgecolor=colors[i])

    


    plt.xlabel("Time [s]", fontsize=9, fontweight='bold')
    plt.ylabel("Signal", fontsize=9, fontweight='bold')
    plt.title("Window Selection", fontsize=11, fontweight='bold')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
