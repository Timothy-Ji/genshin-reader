import cv2 as cv
import numpy as np
import easyocr
import sys
import argparse
import time
import json
import textwrap

start = time.time()

reader = easyocr.Reader(['en'], False)

input_img = ''
res = 1080

parser = argparse.ArgumentParser(sys.argv)
parser.add_argument("img", help="Image source path.", type=str)
parser.add_argument(
    "res", help="Resolution of the game instance the image was taken from.", type=int)
args = parser.parse_args()

input_img = args.img
res = args.res

with open("reader.json") as f:
    readerdata = json.load(f)
with open("items\\items.json") as f:
    itemdata = json.load(f)
with open("naming.json") as f:
    namingdata = json.load(f)

print("Engine:Version=" + readerdata['version'])
print("Item List:Version=" + itemdata['version'])
print("Naming Scheme:Version=" + namingdata['scheme'])

item_list = itemdata['items']
img = cv.imread(input_img)

scale = 1080/res
img = cv.resize(img, (int(img.shape[1]*scale), int(img.shape[0]*scale)))

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
for item in item_list:
    name = namingdata[item]
    print(name)
    template = cv.imread("items\\" + item)
    grayTemplate = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
    result = cv.matchTemplate(gray, grayTemplate, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    threshold = 0.9
    loc = np.where(result >= threshold)
    print('Best match top left position: %s' % str(max_loc))
    print('Best match confidence: %s' % max_val)

    h, w, _ = template.shape

    if max_val >= threshold:
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        
        numberl = reader.readtext(gray[bottom_right[1]-int(h*4/5):bottom_right[1], top_left[0]:bottom_right[0]], allowlist='0123456789', detail=0)
        num = -1
        if (len(numberl) > 0):
            num = numberl[0]

        wrapped_name = textwrap.wrap(item + ' ' + str(num), width=15)
        font = cv.FONT_HERSHEY_SIMPLEX
        font_size = 0.5
        font_thickness = 1
        for i, line in enumerate(wrapped_name):
            textsize = cv.getTextSize(line, font, font_size, font_thickness)[0]

            gap = textsize[1] + 10

            y = int((top_left[1] + textsize[1])) + i * gap
            x = int((top_left[0]))
            cv.putText(img, line, (x, y), font,
                        font_size, 
                        (0,0,0), 
                        font_thickness, 
                        lineType = cv.LINE_AA)

end = time.time()
print(end-start)

cv.imshow('Annotated', img)
cv.waitKey(0)