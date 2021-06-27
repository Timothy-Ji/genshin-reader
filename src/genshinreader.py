import cv2 as cv
import easyocr
import sys
import argparse
import time
import json

start = time.time()

input_img = ''
res = 1080

parser = argparse.ArgumentParser(sys.argv)
parser.add_argument("img", help="Image source path.", type=str)
parser.add_argument(
    "-r", "--res", dest="res", default=1080, help="Resolution of the game instance the image was taken from.", type=int)
parser.add_argument(
    "-if", "--include-failed", default=True, dest="include_failed", help="Resolution of the game instance the image was taken from.", type=bool)
args = parser.parse_args()

input_img = args.img
res = args.res
inc_failed = args.include_failed

reader = easyocr.Reader(['en'], False)

with open("reader.json") as f:
    readerdata = json.load(f)
with open("items\\items.json") as f:
    itemdata = json.load(f)
item_list = itemdata['items']
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


def get_quantity(img) -> int:
    number = reader.readtext(img, allowlist='0123456789', detail=0)
    if len(number) > 0:
        return int(number[0])
    return -1


def find_matches(img_gray, item_list, include_failed):
    matched = {}
    for i, item in enumerate(item_list):
        name = get_name(item)
        print(f'{int((i+1)/len(item_list)*100)}% | {i+1}/{len(item_list)}')
        template = cv.imread("items\\" + item, cv.IMREAD_GRAYSCALE)
        match = find(img_gray, template, 0.9)
        if match:
            h, w = template.shape
            top_left = match
            bottom_right = (top_left[0] + w, top_left[1] + h)
            quantity_segment = img_gray[bottom_right[1] -
                                    int(h*4/5):bottom_right[1], top_left[0]:bottom_right[0]]
            quantity = get_quantity(quantity_segment)
            if quantity != -1 or include_failed:
                matched[name] = quantity
    return matched

def match(img, res, include_failed):
    scale = 1080/res

    img = cv.resize(img, (int(img.shape[1]*scale), int(img.shape[0]*scale)))
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    matches = find_matches(gray, item_list, inc_failed)
    return matches
    

print("Engine Version=" + readerdata['version'])
print("List Version=" + itemdata['version'])
print("Naming Scheme=" + namingdata['scheme'])

img = cv.imread(input_img)

matches = match(img, res, inc_failed)

end = time.time()
print("Time Elapsed (s):", end-start)

output = {"engine-version": readerdata['version'], "list-version": itemdata['version'], "naming-scheme": namingdata['scheme'], "materials": {} }
output['materials'] = matches
print(output)