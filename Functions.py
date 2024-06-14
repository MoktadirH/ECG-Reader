

def detect_peaks(ecgSignal,time):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.signal import find_peaks


    # Compute the moving average of the ECG signal
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
    peaks, _ = find_peaks(movingAvg, height=threshold_high, distance=(windowSize//2))

    # Refine peaks using the lower threshold
    refinedPeaks, _ = find_peaks(movingAvg, height=threshold_low, distance=(windowSize//2))

    # Keep only the peaks that satisfy both thresholds
    finalPeaks = np.intersect1d(peaks, refinedPeaks)
    

    return finalPeaks

