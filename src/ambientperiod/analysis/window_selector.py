import numpy as np

def window_selector(fs, T, V, R, vent, vmin, vmax):

    np_samples = int(fs * vent)
    end_index = len(T) - 2 * np_samples + 1

    MT = []
    MV = []
    pos_a = []
    win_ids = []

    for i, a in enumerate(range(0, end_index + 1, np_samples)):
        segment = R[a:a + np_samples]
        if segment.shape[0] < np_samples:
            continue
        if np.all((segment > vmin) & (segment < vmax)):
            t_window = T[a:a + np_samples]
            v_window = V[a:a + np_samples]
            MT.append(t_window)
            MV.append(v_window)
            pos_a.append(a)
            win_ids.append(i)

    MT = np.column_stack(MT) if MT else np.empty((np_samples, 0))
    MV = np.column_stack(MV) if MV else np.empty((np_samples, 0))
    pos_a = np.array(pos_a)
    win_ids = np.array(win_ids)

    return MT, MV, pos_a, win_ids
