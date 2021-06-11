import cv2 as cv
from pytesseract import pytesseract
import numpy as np

target = [220, 229, 233]
p_range = 18
lower = np.array([target[0]-p_range, target[1]-p_range, target[2]-p_range])
upper = np.array([target[0]+p_range, target[1]+p_range, target[2]+p_range])

img = cv.imread("example\gi.png")

mask = cv.inRange(img, lower, upper)
filtered = cv.bitwise_and(img, img, mask=mask)
filteredgray = cv.cvtColor(filtered, cv.COLOR_BGR2GRAY)
thresh = cv.threshold(filteredgray, 200, 255, 0)[1]
contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

for i, contour in enumerate(contours):
    area = cv.contourArea(contour)
    if area > 1000 and hierarchy[0][i][2] == -1:
        (x, y, w, h) = cv.boundingRect(contour)
        slot = img[int(y+2*h/5):y+h, x:x+w]
        slot_gray = cv.cvtColor(slot, cv.COLOR_BGR2GRAY)
        slot_thresh = cv.threshold(slot_gray, 150, 255, cv.THRESH_BINARY)[1]
        cv.rectangle(slot_thresh, (0, 0), (w, h), (255, 255, 255), 2)
        no = pytesseract.image_to_string(slot_thresh, config='digits').strip()
        if no == '':
            pass
        cv.putText(img, no, (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv.LINE_AA, False)
        
cv.imshow("Image", img)
cv.waitKey(0)