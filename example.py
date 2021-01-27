import cv2 as cv
from genshin_reader import InventoryImage

images = [InventoryImage("example\gi.png", 4, 7), InventoryImage("example\gi2.png", 4, 7),
          InventoryImage("example\gi5by2.png", 2, 5), InventoryImage("example\gi720p.png", 4, 7)]
imglst = []
for i in range(len(images)):
    print(f'Processing image {i + 1}/{len(images)}')
    invImg = images[i]
    img = invImg.get_img_with_details()
    imglst.append([invImg.file, img])
print('Finished')
for img in imglst:
    cv.imshow(img[0], img[1])
cv.waitKey(0)