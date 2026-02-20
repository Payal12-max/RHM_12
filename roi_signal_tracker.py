import numpy as np
from collections import deque
from scipy.signal import butter, filtfilt

class ROISignalTracker:
    def __init__(self, buffer_seconds=30, fps=20):
        self.fps = fps
        self.max_len = buffer_seconds * fps
        self.roi_buffers = {
            "forehead": deque(maxlen=self.max_len),
            "left_cheek": deque(maxlen=self.max_len),
            "right_cheek": deque(maxlen=self.max_len)
        }

    def update(self, roi_values_dict):
        """
        roi_values_dict = { "forehead": green_val, "left_cheek": green_val, ... }
        """
        for roi, val in roi_values_dict.items():
            if roi in self.roi_buffers:
                self.roi_buffers[roi].append(val)

    def bandpass_filter(self, signal, lowcut=0.8, highcut=3.0):
        nyq = 0.5 * self.fps
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(2, [low, high], btype='band')
        return filtfilt(b, a, signal)

    def calculate_snr(self, signal):
        if len(signal) < self.fps * 5:  # Require minimum 5 seconds of data
            return 0
        try:
            filtered = self.bandpass_filter(signal)
            signal_power = np.std(filtered) ** 2
            noise_power = np.std(signal - filtered) ** 2
            snr = signal_power / (noise_power + 1e-6)
            return snr
        except:
            return 0

    def get_best_roi(self):
        snr_scores = {}
        for roi, buffer in self.roi_buffers.items():
            signal = np.array(buffer)
            snr = self.calculate_snr(signal)
            snr_scores[roi] = snr
        best_roi = max(snr_scores, key=snr_scores.get)
        return best_roi, snr_scores
