from globalSetting import *

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
    bumps = 0
    for i in range(FIELD_WIDTH - 1):
        bumps += np.abs(peaks[i] - peaks[i + 1])
    return bumps

def getHoles(field, peaks):
    holesPerCol = []
    for col in range(field.shape[1]):
        start = -int(peaks[col])
        if start == 0: # no blocks in this column
            holesPerCol.append(0)
        else:
            holesPerCol.append(np.count_nonzero(field[start:, col] == 0))
    return holesPerCol
    
def getMetrics(field):
    peaks = getPeaks(field)

    highestPeak = np.max(peaks)

    aggregatedHeight = np.sum(peaks)

    bumpiness = getBumpiness(peaks)

    holesPerCol = getHoles(field, peaks)
    holes = np.sum(holesPerCol)
    colsWithHoles = np.count_nonzero(np.array(holesPerCol) > 0)

    return (highestPeak, aggregatedHeight, bumpiness, holes, colsWithHoles)

METRICS_NAMES = ['highestPeak', 'aggregatedHeight', 'bumpiness', 'holes', 'colsWithHoles']
N_INPUT_SIZE = len(METRICS_NAMES)

def getScore(model, field):
    metrics = getMetrics(field)
    return model.activate(np.array(metrics))
    