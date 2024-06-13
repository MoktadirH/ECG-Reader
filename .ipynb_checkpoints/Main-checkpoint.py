import pandas as pd
import OwnFunctions as of
import matplotlib.pyplot as plt

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


plt.plot(ecg.Time, ecg.lead1)