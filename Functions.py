import pandas as pd
from scipy import signal
import neurokit2 as neuro
import numpy as np
import pywt
import Functions as fx
import matplotlib.pyplot as plt

def detectPeaks(ecgSignal,time):
    # Using the Pan-Tompkins algorithm
    #larger window size more smoothing but less visible sharp features, smaller are more sensitive to noise
    #At each point, find average of data in the window to make a "smoother version, the window moves and groups an area into one point to smoothen it out
    #Window size just depends on just the ecg signal
    windowSize = int(0.12 * 200)

    #mode same means that the output has the same length as the input signal, so the actual graph doesnt become shorter or bigger
    #Convolve is how the moving average is computer
    movingAvg = np.convolve(ecgSignal, np.ones(windowSize) / windowSize, mode="same")

    # Calc std dev of moving average
    stdDev = np.std(movingAvg)

    # Set high and low thresholds, and is dynamic so it can be used in many different files
    #A valid r peak comes when it satisfies both thresholds, so that it can get precise with the low value but only goes throigh if the high also allows, letting it refine it further
    threshold_high = 0.6 * stdDev
    threshold_low = 0.4 * stdDev

    # Find peaks in the moving average
    #Distance is half the window size so that it doesnt detect the QRS complex multiple times
    peaks, _ = signal.find_peaks(movingAvg, height=threshold_high, distance=(windowSize//2))

    # Refine peaks using the lower threshold
    refinedPeaks, _ = signal.find_peaks(movingAvg, height=threshold_low, distance=(windowSize//2))

    # Keep only the peaks that satisfy both thresholds
    finalPeaks = np.intersect1d(peaks, refinedPeaks)
    

    return finalPeaks


#Remove noise so it becomes easier to find r peaks
def butterworthFilter(leads, ord):
    order = ord  #What order filter it will create (Butterworth)
    #Creating the butterworth filter
    #btype allows the low frequencies to pass while the higher ones do not
    #Wn is the ratio compared to half the frequency, which in this case is 100. This means anything that is higher than 0.1*100 will be cut out
    #Lower Wn means more filtered data and vice versa
    b, a = signal.butter(order,Wn=0.1, btype="low", analog=False)

    #returns the filtered data
    return signal.filtfilt(b, a, leads)




def hrvMetrics(rrInt):
    # Time-domain metrics, all of these measurements are based on the intervals between the r peaks

    #Standard deviation of the intervals
    sdrr = np.std(rrInt)
    #Root mean square of the differences between the intervals, much better than finding average rr interval
    rmssd = np.sqrt(np.mean(np.diff(rrInt)**2))
    #Pairs of intervals that are longer than 50ms, put into a percentage form
    prr = np.sum(np.abs(np.diff(rrInt)) > 50) / len(rrInt) * 100

    # Frequency-domain metrics, counts how much low and high frequency beats occur

    #Using the welch method to find power specrtral density, allowing us to evaluate how the power is distributed over the frequencies
    #psd can be used to analyze how the energy is distributed, which we need for hrv
    #nperseg is the length of the segment
    f, psd = signal.welch(rrInt, fs=200, nperseg=len(rrInt))

    #Trapz method is an integration method that calculates the area under a specific curve (psd), the values gives us area at the specific frequencies that we need for each
    
    #Very low = Below 0.04Hz
    #Low = 0.04-0.015 Hz
    #High = 0.015-0.4 Hz

    #(psd >= 0.0033)
    vlowPower = np.trapz(psd[psd < 4])
    lowPower = np.trapz(psd[(psd >= 4) & (psd < 15)])
    highPower = np.trapz(psd[(psd >= 15) & (psd < 4)])

    return sdrr,rmssd,prr,vlowPower,lowPower,highPower,psd