import numpy as np

def algorithm_sta_lta(signal: np.ndarray, fs: float, sta_time: float, lta_time: float):
    """
    Optimización fiel del algoritmo MATLAB original.
    Misma lógica, pero con relleno + cumsum vectorizado.
    """
    N = len(signal)
    Nsta = int(fs * sta_time)
    Nlta = int(fs * lta_time)

    # Relleno de borde usando el valor promedio como en MATLAB
    edge_val = abs((signal[0] + signal[1]) / 2.0)
    signal2 = signal**2

    # Rellenar con valores de borde antes del inicio real
    pad_sta = np.full(Nsta, edge_val)
    pad_lta = np.full(Nlta, edge_val)
    padded_sta = np.concatenate((pad_sta, signal2))
    padded_lta = np.concatenate((pad_lta, signal2))

    # Cálculo acumulado
    cumsum_sta = np.cumsum(padded_sta)
    cumsum_lta = np.cumsum(padded_lta)

    # Ventanas de promedio: para i = 0 hasta N-1
    sta = (cumsum_sta[Nsta:Nsta+N] - cumsum_sta[0:N]) / Nsta
    lta = (cumsum_lta[Nlta:Nlta+N] - cumsum_lta[0:N]) / Nlta

    # STA/LTA con protección de división
    with np.errstate(divide='ignore', invalid='ignore'):
        sta_lta = np.where(lta != 0, sta / lta, 0.0)

    return sta_lta, sta, lta
