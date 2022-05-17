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
    
def getRowTransition(area, highest_peak):
    rowTransitions = 0
    # From highest peak to bottom
    for row in range(int(area.shape[0] - highest_peak), area.shape[0]):
        for col in range(1, area.shape[1]):
            if area[row, col] != area[row, col - 1]:
                rowTransitions += 1
    return rowTransitions

def getWells(peaks):
    wells = []
    for i in range(len(peaks)):
        if i == 0:
            w = peaks[1] - peaks[0]
            w = w if w > 0 else 0
            wells.append(w)
        elif i == len(peaks) - 1:
            w = peaks[-2] - peaks[-1]
            w = w if w > 0 else 0
            wells.append(w)
        else:
            w1 = peaks[i - 1] - peaks[i]
            w2 = peaks[i + 1] - peaks[i]
            w1 = w1 if w1 > 0 else 0
            w2 = w2 if w2 > 0 else 0
            w = w1 if w1 >= w2 else w2
            wells.append(w)
    return wells

def getMetrics(field, pointsDiff):
    peaks = getPeaks(field)

    highestPeak = np.max(peaks)

    aggregatedHeight = np.sum(peaks)

    bumpiness = getBumpiness(peaks)

    holesPerCol = getHoles(field, peaks)
    holes = np.sum(holesPerCol)
    colsWithHoles = np.count_nonzero(np.array(holesPerCol) > 0)

    rowTransitions = getRowTransition(field, highestPeak)

    deepestWell = np.max(getWells(peaks))

    numPits = np.count_nonzero(np.count_nonzero(field, axis=0) == 0)

    if pointsDiff != 0:
        linesCleared = np.sqrt(np.divide(pointsDiff, 100))
    else:
        linesCleared = 0

    return (highestPeak, aggregatedHeight, bumpiness, holes, colsWithHoles, rowTransitions, deepestWell, numPits, linesCleared)

METRICS_NAMES = ['highestPeak', 'aggregatedHeight', 'bumpiness', 'holes', 'colsWithHoles', 'rowTransitions', 'deepestWell', 'numPits', 'linesCleared']
N_INPUT_SIZE = len(METRICS_NAMES)

def getScore(model, field, pointsDiff):
    metrics = getMetrics(field, pointsDiff)
    return model.activate(np.array(metrics))

    