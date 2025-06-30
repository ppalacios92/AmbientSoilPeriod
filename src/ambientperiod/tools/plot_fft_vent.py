import numpy as np
import matplotlib.pyplot as plt

def plot_fft_vent(MFX, MFZ):
    n_windows = MFZ.shape[1]
    colors = plt.cm.hsv(np.linspace(0, 1, n_windows))

    plt.figure(figsize=(10, 6))
    for i in range(n_windows):
        plt.plot(MFX[:, i], MFZ[:, i], color=colors[i], alpha=0.6, linewidth=1.0)

    plt.xlabel('Frequency [Hz]', fontweight='bold')
    plt.ylabel('Amplitude [-]', fontweight='bold')
    plt.title('FFT Amplitude Spectrum', fontweight='bold')
    plt.grid(True)
    plt.xlim(left=0)
    plt.tight_layout()
    plt.show()
