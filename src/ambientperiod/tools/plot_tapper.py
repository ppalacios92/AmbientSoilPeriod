import numpy as np
import matplotlib.pyplot as plt

def plot_tapper(u, MV, MT, vent, T, V):
    m, n = MV.shape
    MA = MV * u[:, np.newaxis]
    x = np.linspace(0, 1, m)
    colors = plt.cm.hsv(np.linspace(0, 1, n))

    plt.figure(figsize=(10, 7))
    # plt.suptitle('Turkeywin', fontweight='bold', fontsize=11)

    # --- Subplot 1: Tapper ---
    plt.subplot(2, 1, 1)
    plt.plot(x * m, u, linewidth=2)
    plt.title('Tapper', fontsize=11, fontweight='bold')
    # plt.xlabel('Time [sec]', fontsize=9, fontweight='bold')
    plt.ylabel('Factor', fontsize=9, fontweight='bold')
    label_text = f'Window Tapper with {m} points. R={int(100 * u.sum() / m)}%'
    plt.legend([label_text], loc='lower right')
    plt.grid(True)

    # --- Subplot 2: Signal with windows ---
    plt.subplot(2, 1, 2)
    plt.plot(T, V, color='black', label='Signal')
    minV, maxV = np.min(V), np.max(V)

    for i in range(n):
        x_patch = [MT[0, i], MT[-1, i], MT[-1, i], MT[0, i]]
        y_patch = [minV, minV, maxV, maxV]
        plt.fill(x_patch, y_patch, color=colors[i], alpha=0.35, edgecolor=colors[i])

    for i in range(1, int(T[-1] // vent) + 1):
        plt.axvline(i * vent, color='gray', linestyle='-', linewidth=0.5, alpha=0.4)

    plt.title('Signal', fontsize=11, fontweight='bold')
    plt.xlabel('Time [sec]', fontsize=9, fontweight='bold')
    plt.ylabel('Counts', fontsize=9, fontweight='bold')
    plt.xlim([0, T[-1]])
    plt.ylim([minV, maxV])
    plt.grid(True)

    plt.show()
