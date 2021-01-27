from typing import Any
import cv2 as cv
import pytesseract
from pytesseract.pytesseract import Output


class Rect:
    def __init__(self, x, y, w, h) -> None:
        self.x, self.y, self.w, self.h = x, y, w, h

    def to_xywh(self):
        return self.x, self.y, self.w, self.h


def get_slot_rects(img, rows: int, cols: int) -> list[Rect]:
    edges = cv.Canny(img, 100, 150)

    x, y, w, h = cv.boundingRect(edges)

    rects = []

    slotWidth = w/cols
    slotHeight = h/rows
    for col in range(0, cols):
        cX = int(slotWidth * col)
        for row in range(0, rows):
            cY = int(slotHeight * row)
            slotImg = img[(y + cY):(y + cY + int(slotHeight)),
                          (x + cX):(x + cX + int(slotWidth))]
            slotEdges = cv.Canny(slotImg, 25, 50)
            sX, sY, sW, sH = cv.boundingRect(slotEdges)
            sX, sY = sX + x + cX, sY + y + cY
            rects.append(Rect(sX, sY, sW, sH))
    return rects


def get_digits_from_image(img):
    thresh = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

    # probably a more optimal way to do this.
    # trim image
    borderThresh = 5
    topY, botY = 0, 0
    searchTop, searchBot = True, True
    for y in range(int(thresh.shape[0] / 2)):
        blackTop = 0
        blackBot = 0
        for x in range(thresh.shape[1]):
            if (searchTop):
                pixel = thresh[y, x]
                if (pixel != 255):
                    blackTop += 1
            if (searchBot):
                pixel = thresh[thresh.shape[0] - y - 1, x]
                if (pixel != 255):
                    blackBot += 1
        if (searchTop and blackTop <= borderThresh):
            topY = y
            searchTop = False
        if (searchBot and blackBot <= borderThresh):
            botY = thresh.shape[0] - y - 1
            searchBot = False
        if (not searchTop and not searchBot):
            break
    cropX, cropY, cropW, cropH = int(thresh.shape[1] * 1/10), topY, thresh.shape[1] - int(
        thresh.shape[1] * 2/10), botY
    thresh = thresh[(cropY):(cropY + cropH), (cropX):(cropX + cropW)]

    s = pytesseract.image_to_string(thresh, config='--oem 3 --psm 12 digits')
    s = ''.join(filter(str.isdigit, s))

    return s


class InventoryImage:
    def __init__(self, file: str, invRows: int, invCols: int) -> None:
        self.file = file
        self.rows = invRows
        self.cols = invCols

    def get_img(self):
        return cv.imread(self.file)

    def get_img_with_details(self) -> str:
        img = self.get_img()        
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        slotrects = get_slot_rects(img, self.rows, self.cols)
        
        for i in range(len(slotrects)):
            rect = slotrects[i]
            cv.rectangle(img, (rect.x, rect.y), (rect.x + rect.w, rect.y + rect.h), (0, 0, 255), 2)

            # kind of assumes location, gets bottom 1/5th of image
            splicedrect = Rect(rect.x, rect.y + int(rect.h * 4 / 5), rect.w, rect.h - int(rect.h * 4 / 5))
            cv.rectangle(img, (splicedrect.x, splicedrect.y), (splicedrect.x + splicedrect.w, splicedrect.y + splicedrect.h), (0, 255, 0), 2)

            slotgray = gray[(splicedrect.y):(splicedrect.y+splicedrect.h), (splicedrect.x):(splicedrect.x+splicedrect.w)]
            s = get_digits_from_image(slotgray)
            cv.putText(img, s, (rect.x, rect.y + 25), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2, cv.LINE_AA)
        return img
