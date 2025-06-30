import numpy as np
from scipy.signal import butter, filtfilt, detrend

def fft_vent(fs, ma, apply_filter=False, f1=1.0, f2=4.0):
    n_samples, n_windows = ma.shape
    nfft = 2**15
    freqs = np.fft.fftfreq(nfft, d=1/fs)[:nfft // 2]

    MFX = np.tile(freqs[:, None], (1, n_windows))
    MFY = np.zeros((nfft // 2, n_windows), dtype=np.complex64)
    MFZ = np.zeros((nfft // 2, n_windows), dtype=np.float64)

    if apply_filter:
        wn = [f1, f2]
        wn = [w / (fs / 2) for w in wn]
        b, a = butter(4, wn, btype='band')

    for j in range(n_windows):
        amp = ma[:, j].copy()
        amp = detrend(amp)
        if apply_filter:
            amp = filtfilt(b, a, amp)
        amp = amp - np.mean(amp)
        spectrum = np.fft.fft(amp, n=nfft)[:nfft // 2]
        MFY[:, j] = spectrum
        MFZ[:, j] = np.abs(spectrum)

    return MFX, MFY, MFZ
