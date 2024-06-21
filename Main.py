import pandas as pd
import matplotlib.pyplot as plt
import Functions as fx

columns = ["lead1","lead2", "lead3", "Time"]
time=0
timeCheck=5 #File is 200Hz, which means that each line is 5ms away from each other

#Reading the file and storing it into a variable that we can play around with
ecg=pd.read_csv("1-300m.txt",names=columns, sep="\t")

#Finding out how many rows were read so that we can make the time column based on that since the file does not contain that
rowCount = ecg.shape[0]
times = range(0, rowCount * timeCheck, timeCheck)
ecg["Time"] = list(times)

filteredEcg = pd.DataFrame()
filteredEcg["Time"] = ecg["Time"]

# Apply the filter to lead1 data
filteredEcg["lead1"] = fx.butterworthFilter(ecg.lead1,4)
filteredEcg["lead2"] = fx.butterworthFilter(ecg.lead2,4)
filteredEcg["lead3"] = fx.butterworthFilter(ecg.lead3,4)


rPeaks=fx.detectPeaks(filteredEcg.lead1,filteredEcg.Time)
#sdrr,rmssd,prr,vLowPower,lowPower,highPower
sdrr,rmssd,prr,vLowPower,lowPower,highPower,psd=fx.hrvMetrics(rPeaks)

print(vLowPower)
plt.figure()
plt.plot(psd)
"""plt.plot(filteredEcg.Time, filteredEcg.lead1, label="Lead 1")
#Since derivative changes the size, the -4 calibrates it back from the sine graph to the actual graph
plt.scatter(filteredEcg.Time[rPeaks], filteredEcg.lead1[rPeaks], color="r", marker="o", label="R-peaks")
plt.xlabel("Time (ms)")
plt.ylabel("Amplitude (mV)")
plt.title("ECG Signal with R-peaks")
plt.legend()"""
plt.show()