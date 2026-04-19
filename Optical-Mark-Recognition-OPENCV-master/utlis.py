# utlis.py - Utility functions for OMR (Optimized & Stable)
import cv2
import numpy as np

def stackImages(imgArray, scale, labels=[]):
    rows = len(imgArray)
    cols = len(imgArray[0]) if rows > 0 else 0
    if rows == 0 or cols == 0:
        return np.zeros((200, 400, 3), dtype=np.uint8) + 255
    
    try:
        h, w = imgArray[0][0].shape[:2]
    except:
        return np.zeros((200, 400, 3), dtype=np.uint8) + 255

    for x in range(rows):
        for y in range(cols):
            if imgArray[x][y] is None or imgArray[x][y].size == 0:
                imgArray[x][y] = np.zeros((h, w, 3), dtype=np.uint8) + 255
                continue
            imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
            if len(imgArray[x][y].shape) == 2:
                imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)

    hor = [np.hstack(row) for row in imgArray]
    ver = np.vstack(hor)

    if labels and len(labels) == rows:
        eachW, eachH = int(ver.shape[1]/cols), int(ver.shape[0]/rows)
        for i in range(rows):
            for j in range(cols):
                if j < len(labels[i]):
                    txt = labels[i][j]
                    cv2.rectangle(ver, (j*eachW, i*eachH),
                                  (j*eachW + len(txt)*13 + 27, i*eachH + 30),
                                  (255, 255, 255), -1)
                    cv2.putText(ver, txt, (j*eachW + 10, i*eachH + 20),
                                cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 255), 2)
    return ver

def reorder(myPoints):
    if myPoints is None or len(myPoints) != 4: return None
    myPoints = myPoints.reshape((4, 2))
    newPoints = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)
    diff = np.diff(myPoints, axis=1)
    newPoints[0] = myPoints[np.argmin(add)]
    newPoints[3] = myPoints[np.argmax(add)]
    newPoints[1] = myPoints[np.argmin(diff)]
    newPoints[2] = myPoints[np.argmax(diff)]
    return newPoints

def rectContour(contours, minArea=1000):
    rectCon = []
    for c in contours:
        if cv2.contourArea(c) > minArea:
            if len(cv2.approxPolyDP(c, 0.02*cv2.arcLength(c, True), True)) == 4:
                rectCon.append(c)
    return sorted(rectCon, key=cv2.contourArea, reverse=True)

def getCornerPoints(cont):
    if cont is None or len(cont) == 0: return None
    approx = cv2.approxPolyDP(cont, 0.02*cv2.arcLength(cont, True), True)
    return approx if len(approx) == 4 else None

def splitBoxes(img, rows=5, cols=5):
    boxes = []
    for r in np.vsplit(img, rows):
        boxes.extend(np.hsplit(r, cols))
    return boxes

def drawGrid(img, q=5, c=5):
    secW, secH = int(img.shape[1]/c), int(img.shape[0]/q)
    for i in range(q+1):
        cv2.line(img, (0, i*secH), (img.shape[1], i*secH), (255,255,0), 2)
    for i in range(c+1):
        cv2.line(img, (i*secW, 0), (i*secW, img.shape[0]), (255,255,0), 2)
    return img

def showAnswers(img, myIndex, grading, ans, q=5, c=5):
    secW, secH = int(img.shape[1]/c), int(img.shape[0]/q)
    for x in range(q):
        cX, cY = (myIndex[x]*secW)+secW//2, (x*secH)+secH//2
        color = (0,255,0) if grading[x]==1 else (0,0,255)
        if grading[x]==0:
            cv2.circle(img, ((ans[x]*secW)+secW//2, (x*secH)+secH//2), 20, (0,255,0), cv2.FILLED)
        cv2.circle(img, (cX, cY), 40, color, cv2.FILLED)
    return img
    print("ok")