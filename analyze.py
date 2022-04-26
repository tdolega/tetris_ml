from globalSetting import *

def getMetrics(field):
    peaks = getPeaks(field)

    highestPeak = np.max(peaks)
    logging.debug('highestPeak: %d', highestPeak)

    aggregatedHeight = np.sum(peaks)
    logging.debug('aggregatedHeight: %d', aggregatedHeight)

    bumpiness = getBumpiness(peaks)
    logging.debug('bumpiness: %d', bumpiness)

    return (highestPeak, aggregatedHeight, bumpiness)

def getPeaks(area):
    peaks = np.array([])
    for col in range(area.shape[1]):
        if 1 in area[:, col]:
            p = area.shape[0] - np.argmax(area[:, col], axis=0)
            peaks = np.append(peaks, p)
        else:
            peaks = np.append(peaks, 0)
    return peaks

def getBumpiness(peaks):
    s = 0
    for i in range(9):
        s += np.abs(peaks[i] - peaks[i + 1])
    return s