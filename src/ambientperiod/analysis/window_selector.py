# Select valid signal windows based on STA/LTA ratio

import numpy as np

def window_selector(signal, ratio, fs, vent, vmin, vmax):
    n = len(signal)
    n_points = int(fs * vent)
    t = np.arange(n) / fs

    windows_time = []
    windows_signal = []
    positions = []

    for start in range(0, n - 2 * n_points + 1, n_points):
        segment = ratio[start:start + n_points]
        if np.all((segment > vmin) & (segment < vmax)):
            t_window = t[start:start + n_points]
            v_window = signal[start:start + n_points]
            windows_time.append(t_window)
            windows_signal.append(v_window)
            positions.append(start)

    MT = np.column_stack(windows_time) if windows_time else np.empty((n_points, 0))
    MV = np.column_stack(windows_signal) if windows_signal else np.empty((n_points, 0))
    pos_a = np.array(positions)

    return MT, MV, pos_a
