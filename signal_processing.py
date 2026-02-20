import numpy as np
from scipy.signal import butter, filtfilt, find_peaks

class SignalProcessor:
    def __init__(self, fps):
        self.fps = fps
        self.lowcut = 0.8
        self.highcut = 3.0
        self.buffer = []

    def bandpass_filter(self, signal):
        nyq = 0.5 * self.fps
        b, a = butter(3, [self.lowcut / nyq, self.highcut / nyq], btype='band')
        return filtfilt(b, a, signal)

    def calculate_hr_and_hrv(self, signal):
        if len(signal) < self.fps * 5:
            return None, None
        try:
            filtered = self.bandpass_filter(np.array(signal))
            peaks, _ = find_peaks(filtered, distance=int(self.fps / 2.5))
            if len(peaks) < 2:
                return None, None

            rr_intervals = np.diff(peaks) / self.fps
            hr = 60 / np.mean(rr_intervals)
            hrv_sdnn = np.std(rr_intervals) * 1000
            return hr, hrv_sdnn
        except:
            return None, None

