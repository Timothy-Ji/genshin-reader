import cv2 as cv
import numpy as np
import easyocr
import sys
import argparse
import time

QUANTITY_BGCOLOR_BGR = [220, 229, 233]
QUANTITY_BGCOLOR_RANGE = 18

reader = easyocr.Reader(['en'], False)

class _Slot:
    def __init__(self, item_name: str, quantity: int) -> None:
        self.item_name = item_name
        self.quantity = quantity


def annotate(img, res=1080):
    lower = np.array(
        [QUANTITY_BGCOLOR_BGR[0]-QUANTITY_BGCOLOR_RANGE, QUANTITY_BGCOLOR_BGR[1]-QUANTITY_BGCOLOR_RANGE, QUANTITY_BGCOLOR_BGR[2]-QUANTITY_BGCOLOR_RANGE])
    upper = np.array(
        [QUANTITY_BGCOLOR_BGR[0]+QUANTITY_BGCOLOR_RANGE, QUANTITY_BGCOLOR_BGR[1]+QUANTITY_BGCOLOR_RANGE, QUANTITY_BGCOLOR_BGR[2]+QUANTITY_BGCOLOR_RANGE])

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    mask = cv.inRange(img, lower, upper)
    filtered = cv.bitwise_and(gray, gray, mask=mask)
    contours, hierarchy = cv.findContours(
        filtered, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    min_area = res * 1.5
    avgs = 0
    avgc = 0

    cv.drawContours(img, contours, -1, (255, 0, 0), 2)

    for i, contour in enumerate(contours):
        area = cv.contourArea(contour)
        if area > min_area and hierarchy[0][i][2] == -1:
            avgs += area
            avgc += 1
            (x, y, w, h) = cv.boundingRect(contour)
            if h < res / 10:
                item_img = img[y-int(h*2.3):int(y+2*h/5), x:x+w]
                quantity_img = img[int(y+2*h/5):y+h, x:x+w]
            else:
                item_img = img[y:int(y+4*h/5), x:x+w]
                quantity_img = img[int(y+4*h/5):y+h, x:x+w]
                y = int(y+3*h/5)

            slot = _process_slot(item_img, quantity_img)
            if int(slot.quantity) > 0:
                cv.putText(img, str(slot.quantity), (x, y), cv.FONT_HERSHEY_SIMPLEX,
                           1, (0, 0, 0), 2, cv.LINE_AA, False)

            # TODO: remove.
            progress = int(i/len(contours) * 100)
            print("Processed: " + str(progress) + "% ")
    print(str(avgs/avgc))
    return img


def _process_slot(item_img, quantity_img) -> _Slot:
    quantity = _read_number(quantity_img)
    return _Slot('', quantity)


def _read_number(img) -> int:
    numberl = reader.readtext(img, allowlist='0123456789', detail=0)
    if (len(numberl) > 0):
        return numberl[0]
    else:
        return -1


def _match_image(img) -> str:
    pass


## Testing Example.
def example(img_path, res):
    start = time.time()

    eimg = cv.imread(img_path)

    scale = 1080/res
    eimg = cv.resize(eimg, (int(eimg.shape[1]*scale), int(eimg.shape[0]*scale)))
    img_res = 1080

    anno = annotate(eimg, res)

    end = time.time()

    print(end-start)

    cv.imshow('Annotated', anno)
    cv.waitKey(0)

input_img = ''
res = 1080

parser = argparse.ArgumentParser(sys.argv)
parser.add_argument("img", help="Image source path.", type=str)
parser.add_argument("res", help="Resolution of the game instance the image was taken from.", type=int)
args = parser.parse_args()

input_img = args.img
res = args.res

example(input_img, res)