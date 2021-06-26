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

with open("naming.json") as f:
    namingdata = json.load(f)
def get_name(key: str) -> str:
    """Returns name of item."""
    return namingdata['map'][key]

def find(img, look_for, threshold: float):
    """Looks for best matching <look_for> in <img> above <threshold>."""
    result = cv.matchTemplate(img, look_for, cv.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv.minMaxLoc(result)
    if max_val >= threshold:
        return max_loc
    return None

def get_quantity(img):
    number = reader.readtext(gray[bottom_right[1]-int(h*4/5):bottom_right[1], top_left[0]:bottom_right[0]], allowlist='0123456789', detail=0)
    if len(number) > 0:
        return number[0]
    return -1

def add_text_to_img(img, name, num, top_left):
    wrapped_name = textwrap.wrap(name + ' ' + str(num), width=14)

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

print("Engine:Version=" + readerdata['version'])
print("Item List:Version=" + itemdata['version'])
print("Naming Scheme:Version=" + namingdata['scheme'])

item_list = itemdata['items']
img = cv.imread(input_img)

scale = 1080/res

img = cv.resize(img, (int(img.shape[1]*scale), int(img.shape[0]*scale)))
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

for item in item_list:
    name = get_name(item)
    print(name)

    template = cv.imread("items\\" + item, cv.IMREAD_GRAYSCALE)
    
    match = find(gray, template, 0.9)
    if match:
        h, w = template.shape
        top_left = match
        bottom_right = (top_left[0] + w, top_left[1] + h)
        
        quantity_segment = gray[bottom_right[1]-int(h*4/5):bottom_right[1], top_left[0]:bottom_right[0]]

        num = get_quantity(quantity_segment)

        add_text_to_img(img, name, num, top_left)

end = time.time()
print(end-start)

cv.imshow('Annotated', img)
cv.waitKey(0)