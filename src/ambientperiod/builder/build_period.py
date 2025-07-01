import numpy as np


from ambientperiod.preprocessing.load_utils import load_utils



from ambientperiod.analysis.algorithm_sta_lta import algorithm_sta_lta
from ambientperiod.analysis.window_selector import window_selector
from ambientperiod.analysis.taper_function import taper_function
from ambientperiod.analysis.fft_vent import fft_vent
from ambientperiod.analysis.sua_vent import sua_vent
from ambientperiod.analysis.prom_vent import prom_vent



from ambientperiod.tools.plot_sta_lta import plot_sta_lta
from ambientperiod.tools.plot_windows_selected import plot_windows_selected
from ambientperiod.tools.plot_tapper import plot_tapper
from ambientperiod.tools.plot_spectrum import plot_spectrum

from ambientperiod.tools.plot_peak_kde import plot_peak_kde



class BuildPeriod:
    def __init__(self, signal_path, config):
        self.signal_path = signal_path
        self.config = config
        self.signal = None
        self.windows = None
        self.spectra = []
        self.periods = []
        self.mean_spectrum = None




        self.load_signal()
        
        self.algorithm_sta_lta()
        self.window_selector()
        self.plot_selected_windows()

        self.taper_function()
        self.plot_tapper()


        self.compute_fft()

        self.sua_vent()
        self.prom_vent()

        self.plot_spectrum()
        self.plot_peak_kde()









    def load_signal(self):
        self.signal = load_utils(self.signal_path)
        print('load_signal OK...')

    def algorithm_sta_lta(self):
        v = (self.signal - np.mean(self.signal)) / np.std(self.signal)
        v = v / np.max(np.abs(v))
        fs = self.config["Fs"]
        sta = self.config["STA"]
        lta = self.config["LTA"]
        sta_lta, sta_vals, lta_vals = algorithm_sta_lta(v, fs, sta, lta)
        self.sta_lta = sta_lta
        self.sta = sta_vals
        self.lta = lta_vals
        print('algorithm_sta_lta OK...')
        self.plot_sta_lta()
        print('plot_sta_lta OK...')

    def window_selector(self):
        fs = self.config["Fs"]
        vmin = self.config["vmin"]
        vmax = self.config["vmax"]
        vent = self.config["vent"]

        MT, MV, pos_a = window_selector(self.signal, self.sta_lta, fs, vent,  vmin, vmax )
        self.windows_time = MT
        self.windows_signal = MV
        self.windows_pos = pos_a
        print('window_selector OK...')


    def taper_function(self):
        p = self.config["p"]
        self.windows_signal_tapered, self.taper_window = taper_function(self.windows_signal, p)
        print('taper_function OK...')

    def compute_fft(self):
        fs = self.config["Fs"]
        apply_filter = self.config.get("apply_filter", "N")
        f1 = self.config.get("f1", 1.0)
        f2 = self.config.get("f2", 4.0)

        mfx, mfy, mfz = fft_vent(fs, self.windows_signal, apply_filter, f1, f2)
        self.mfx = mfx
        self.mfy = mfy
        self.mfz = mfz
        print('compute_fft OK...')

    def sua_vent(self):
        bexp = self.config["bexp"]
        self.mfs = sua_vent(self.mfx, self.mfz, bexp)
        print('sua_vent OK...')

    def prom_vent(self):
        self.mean_spectrum = prom_vent(self.mfs)
        print('prom_vent OK...')















    def plot_sta_lta(self):
        fs = self.config["Fs"]
        vmin = self.config["vmin"]
        vmax = self.config["vmax"]
        vent = self.config["vent"]

        plot_sta_lta(self.signal,  self.sta,  self.lta, self.sta_lta,  fs,  vmin,  vmax,  vent  )

    def plot_selected_windows(self):
        fs = self.config["Fs"]

        plot_windows_selected( self.signal, self.windows_time, self.windows_signal,  fs )
        print('plot_selected_windows OK...')

    def plot_tapper(self):
        fs = self.config["Fs"]

        plot_tapper(self.taper_window, self.windows_signal, self.windows_time, self.config["vent"], 
                    np.arange(len(self.signal)) / fs, self.signal)
        print('plot_tapper OK...')


    def plot_spectrum(self):
        self.mean_spectrum = prom_vent(self.mfs)
        peak_spacing_hz = 0.2
        plot_spectrum(self.mfx, self.mfs, self.mean_spectrum, peak_spacing_hz=peak_spacing_hz)

        print('prom_vent OK...')

    def plot_peak_kde(self):
        ...
        # plot_peak_kde(self.mfx, self.mfs, self.config["vent"], self.config["Fs"], bins=40)
        # print('plot_peak_kde OK...')
