import numpy as np
import cv2 as cv

def isolate_slots(img_path: str, rows: int, cols: int):
    img = cv.imread(img_path)
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    edges = cv.Canny(gray, 100, 150)

    x, y, w, h = cv.boundingRect(edges)

    slotWidth = w/cols
    slotHeight = h/rows
    for col in range(0, cols):
        cX = int(slotWidth * col)
        for row in range(0, rows):
            cY = int(slotHeight * row)
            slotImg = gray[(y + cY):(y + cY + int(slotHeight)),
                           (x + cX):(x + cX + int(slotWidth))]
            slotEdges = cv.Canny(slotImg, 25, 50)
            sX, sY, sW, sH = cv.boundingRect(slotEdges)
            sX, sY = sX + x + cX, sY + y + cY
            cv.rectangle(img, (sX, sY), (sX + sW, sY + sH), (0, 0, 255), 2)
    return img


class InventoryImage:
    def __init__(self, file: str, invRows: int, invCols: int) -> None:
        self.file = file
        self.invRows = invRows
        self.invCols = invCols

    def display_highlighted_slots(self) -> str:
        img = isolate_slots(self.file, self.invRows, self.invCols)
        winname = self.file[:self.file.index(".")]
        cv.imshow(winname, img)
        return winname


images = [InventoryImage("gi.png", 4, 7), InventoryImage("gi2.png", 4, 7),
          InventoryImage("gi5by2.png", 2, 5), InventoryImage("gi720p.png", 4, 7)]

for invImg in images:
    winname = invImg.display_highlighted_slots()
    cv.waitKey(0)
    cv.destroyWindow(winname)
