import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def plot_spectrum(mfx, mfs, mfp, peak_spacing_hz=0.5, numer_peaks=4,
                  min_freq=0.0, xlim=None, ylim=None):

    f = mfx[:, 0] if mfx.ndim == 2 else mfx
    df = f[1] - f[0]
    min_dist = int(peak_spacing_hz / df)

    plt.figure(figsize=(10, 3), facecolor='white')

    # Espectros individuales
    if mfs.ndim == 2:
        for i in range(mfs.shape[1]):
            plt.semilogx(f, mfs[:, i], color='lightgray', alpha=0.4)
    else:
        plt.semilogx(f, mfs, color='lightgray', alpha=0.4)

    # Espectro promedio
    avg_line, = plt.semilogx(f, mfp, color='steelblue', linewidth=2, label='Average Spectrum')

    # Detectar picos
    peaks, _ = find_peaks(mfp, distance=min_dist)

    # Filtrar por frecuencia mínima
    peaks = [p for p in peaks if f[p] >= min_freq]

    # Ordenar picos por amplitud (descendente), tomar los más altos
    top_peaks = sorted(peaks, key=lambda i: mfp[i], reverse=True)[:numer_peaks]

    # Orden final por frecuencia creciente
    # top_peaks = sorted(sorted_peaks[:numer_peaks], key=lambda i: f[i])

    # Dibujar picos
    pastel = ['mediumaquamarine', 'lightcoral', 'cornflowerblue', 'plum']
    lines = []
    for i, idx in enumerate(top_peaks):
        fi = f[idx]
        amp = mfp[idx]
        Ti = 1.0 / fi if fi != 0 else 0.0
        color = pastel[i % len(pastel)]
        mark, = plt.plot(fi, amp, 'o', color=color, markersize=6)
        lines.append((mark, f'Peak {i+1}: f = {fi:.2f} Hz / T = {Ti:.2f} s'))

    # Etiquetas y formato
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.xlabel('Frequency [Hz]', fontweight='bold')
    plt.ylabel('Amplitude', fontweight='bold')
    plt.title('Spectrum and Average (All Windows)', fontweight='bold')

    if xlim: plt.xlim(xlim)
    if ylim: plt.ylim(ylim)

    # Leyenda
    handles = [avg_line] + [l for l, _ in lines]
    labels = ['Average Spectrum'] + [txt for _, txt in lines]
    plt.legend(handles, labels, loc='upper right', fontsize=9)

    plt.tight_layout()
    plt.show()

    print("\n📊 Peaks")
    df_peaks = pd.DataFrame({
        'Peak #': [f'Peak {i+1}' for i in range(len(top_peaks))],
        'Frequency [Hz]': [f[idx] for idx in top_peaks],
        'Period [s]': [1.0 / f[idx] if f[idx] != 0 else 0.0 for idx in top_peaks],
        'Amplitude': [mfp[idx] for idx in top_peaks]
    })

    print(df_peaks.to_string(index=False))
