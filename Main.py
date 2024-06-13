import pandas as pd
import Functions as of
import matplotlib.pyplot as plt
from scipy import signal
import neurokit2 as neuro
import numpy as np
import pywt

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
b, a = signal.butter(order,0.1, btype="low", analog=False)

#Remove noise and other things just to make it easier
filteredEcg = pd.DataFrame()
filteredEcg["Time"] = ecg["Time"]

# Apply the filter to lead1 data
filteredEcg["lead1"] = signal.filtfilt(b, a, ecg.lead1)
filteredEcg["lead2"] = signal.filtfilt(b, a, ecg.lead2)
filteredEcg["lead3"] = signal.filtfilt(b, a, ecg.lead3)


#Following Pan-Tompkins algorithm
#Change Height accordingly since we do not know if the bottom ones are needed
peaks1,_=signal.find_peaks(filteredEcg.lead1, height=0.2)
peaks2,_=signal.find_peaks(filteredEcg.lead2, height=0.2)
peaks3,_=signal.find_peaks(filteredEcg.lead3, height=0.2)


#Following Pan-Tompkins algorithm
#Differentiating and squaring the filtered ecg as lead 1 only, helps really find those peak slopes which are the r peaks, make it more visible
diffEcg=np.diff(filteredEcg.lead1)
squaredEcg = diffEcg ** 2

#larger window size more smoothing but less visible sharp features, smaller are more sensitive to noise
#At each point, find average of data in the window to make a "smoother version, the window moves and groups an area into one point to smoothen it out
#0.12 seconds is usually the duration of the QRS complex
windowSize = int(0.12 * 200)  # Adjust to whatever works

#mode same means that the output has the same length as the input signal, so the actual graph doesnt become shorter or bigger
#Convolve is how the moving average is computer
movingAverage = np.convolve(squaredEcg, np.ones(windowSize) / windowSize, mode="same")

# Thresholding to distinguish the r peaks, value depends on other factors and higher may miss actual r peaks but get rid of noise
threshold = 0.0005
#index 0 since where function gives a tuple of arrays and we just need the first one since it is a 1d array
rPeaks = np.where(movingAverage> threshold)[0]


plt.figure()
plt.plot(filteredEcg.Time, filteredEcg.lead1, label="Lead 1")
plt.scatter(filteredEcg.Time[rPeaks], filteredEcg.lead1[rPeaks], color="r", marker="o", label="R-peaks")
plt.xlabel("Time (ms)")
plt.ylabel("Amplitude (mV)")
plt.title("ECG Signal with R-peaks")
plt.legend()
plt.show()