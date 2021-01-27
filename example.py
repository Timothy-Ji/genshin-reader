from genshin_reader import InventoryImage
import cv2 as cv

images = [InventoryImage("example\gi.png", 4, 7), InventoryImage("example\gi2.png", 4, 7),
          InventoryImage("example\gi5by2.png", 2, 5), InventoryImage("example\gi720p.png", 4, 7)]

for invImg in images:
    winname = invImg.display_highlighted_slots()
    cv.waitKey(0)
    cv.destroyWindow(winname)
