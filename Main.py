import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import neurokit2 as neuro
import numpy as np
import pywt
import Functions as fx

columns = ["lead1","lead2", "lead3", "Time"]
time=0
timeCheck=5


def strip(text):
    try:
        return text.strip()
    except AttributeError:
        return text

ecg=pd.read_csv("1-300m.txt",names=columns, sep="\t")

rowCount = ecg.shape[0]
times = range(0, rowCount * timeCheck, timeCheck)
ecg["Time"] = list(times)

order = 4  #4th order Filter (Butterworth)
b, a = signal.butter(order,0.09, btype="low", analog=False)

#Remove noise and other things just to make it easier
filteredEcg = pd.DataFrame()
filteredEcg["Time"] = ecg["Time"]

# Apply the filter to lead1 data
filteredEcg["lead1"] = signal.filtfilt(b, a, ecg.lead1)
filteredEcg["lead2"] = signal.filtfilt(b, a, ecg.lead2)
filteredEcg["lead3"] = signal.filtfilt(b, a, ecg.lead3)


rPeaks=fx.detect_peaks(filteredEcg.lead1)

plt.figure()
plt.plot(filteredEcg.Time, filteredEcg.lead1, label="Lead 1")

#Since derivative changes the size, the -4 calibrates it back from the sine graph to the actual graph
plt.scatter(filteredEcg.Time[rPeaks], filteredEcg.lead1[rPeaks], color="r", marker="o", label="R-peaks")
plt.xlabel("Time (ms)")
plt.ylabel("Amplitude (mV)")
plt.title("ECG Signal with R-peaks")
plt.legend()
plt.show()