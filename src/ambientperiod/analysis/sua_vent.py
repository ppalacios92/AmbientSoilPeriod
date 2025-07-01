import numpy as np
import matplotlib.pyplot as plt
from numba import njit

@njit
def _sua_vent(mfx, mfz, bexp):
    mm, nn = mfz.shape
    mfs = np.zeros_like(mfz)

    for j in range(nn):
        y = mfz[:, j]
        f = mfx[:, j]

        nx = len(f)
        dx = f[1] - f[0]
        fratio = 10 ** (2.5 / bexp)

        for ix in range(nx):
            fc = f[ix]
            if fc <= 0:
                continue

            ix1 = max(int(fc / fratio / dx), 1)
            ix2 = min(int(fc * fratio / dx + 1), nx - 1)

            a1 = 0.0
            a2 = 0.0

            for jx in range(ix1, ix2 + 1):
                if jx != ix and f[jx] > 0:
                    log_ratio = np.log10(f[jx] / fc)
                    d = log_ratio * bexp
                    if d != 0.0:
                        s = np.sin(d)
                        c = (s / d) ** 4
                    else:
                        c = 1.0
                else:
                    c = 1.0
                a1 += c * y[jx]
                a2 += c

            mfs[ix, j] = a1 / a2 if a2 != 0 else 0.0

    return mfs

def sua_vent(mfx, mfz, bexp):
    """
    Aplica el suavizado Konno-Ohmachi a un espectro por ventanas.
    - Si `mfx` es un vector 1D, lo replica automáticamente por columnas.
    - Retorna el espectro suavizado `mfs`.
    """
    if mfx.ndim == 1:
        mfx = np.tile(mfx[:, None], mfz.shape[1])
    return _sua_vent(mfx, mfz, bexp)

# ------------------------------------------------------------
# (Opcional) Ilustración automática para verificar suavizado
# ------------------------------------------------------------
def show_smoothing_example():
    f = np.linspace(0.14, 0.32, 1000)
    signal = 3 + 1.5 * np.cos(40 * np.pi * f)

    R_values = [20, 40, 60, 80, 100]
    smoothed_spectra = []

    for R in R_values:
        smoothed = np.zeros_like(f)
        for i, fc in enumerate(f):
            x = np.log10(f / fc)
            with np.errstate(divide='ignore', invalid='ignore'):
                w = np.where(
                    x == 0,
                    1.0,
                    (np.sin(R * x) / (R * x))**4
                )
            smoothed[i] = np.sum(w * signal) / np.sum(w)
        smoothed_spectra.append(smoothed)

    plt.figure(figsize=(10, 3))
    plt.plot(f, signal, label='Original Signal', linewidth=2)
    for R, smoothed in zip(R_values, smoothed_spectra):
        plt.plot(f, smoothed, label=f'R={R}')
    plt.xlabel('Frequency [Hz]', fontweight='bold')
    plt.ylabel('Amplitude', fontweight='bold')
    plt.title('Konno-Ohmachi Smoothing Example', fontweight='bold')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
