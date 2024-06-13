import pandas as pd
import OwnFunctions as of
import matplotlib.pyplot as plt
from scipy import signal

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
b, a = signal.butter(order,0.3, btype="low", analog=False)

#Remove noise and other things just to make it easier
filteredEcg = pd.DataFrame()
filteredEcg["Time"] = ecg["Time"]

# Apply the filter to lead1 data
filteredEcg["lead1"] = signal.filtfilt(b, a, ecg["lead1"])
filteredEcg["lead2"] = signal.filtfilt(b, a, ecg["lead2"])
filteredEcg["lead3"] = signal.filtfilt(b, a, ecg["lead3"])

plt.figure()


plt.plot(ecg.Time, ecg.lead1, label="or Lead 1")
plt.plot(filteredEcg.Time, filteredEcg.lead1, label="Filtered Lead 1")

plt.xlabel("Time (ms)")
plt.ylabel("Amplitude (mV)")
plt.title("ECG Data")
plt.legend()
plt.show()