import imutils
import argparse
import time
import cv2
from classify import analyse

def pyramid(image, scale=1.5, minSize=(30, 30)):
	yield image
	while True:
		w = int(image.shape[1] / scale)
		image = imutils.resize(image, width=w)
		if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
			break
		yield image
def sliding_window(image, stepSize, windowSize):
	for y in range(0, image.shape[0], stepSize):
		for x in range(0, image.shape[1], stepSize):
			yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])


resim = image
mx = 0

(winW, winH) = (128, 128)
say = 0
xx = 0
yy = 0
saybul = 0

for resized in pyramid(image, scale=1.5):
	say += 1
	print(resized.shape)
	if(resized.shape[0] > 300):
		continue
	for (x, y, window) in sliding_window(resized, stepSize=16, windowSize=(winW, winH)):
		if window.shape[0] != winH or window.shape[1] != winW:
			continue
		ara = resized[y : y + winH,x : x + winW]
		_, a_numpy = cv2.imencode('.jpg', ara)

		obj = analyse(a_numpy.tobytes())
		if (obj['plastic'] > mx):
			mx = obj['plastic']
			resim = ara
			xx = x
			yy = y
			saybul = say


# cv2.imshow("Window", resim)
crp =  pow(1.5, saybul - 1)
print(image.shape)
print(int(yy*crp) , int(yy * crp) + winH, int(xx*crp) , int(xx*crp) + winW )
print(xx, yy)
print(say, crp)
cv2.rectangle(image, (int(xx * crp), int(yy * crp)), (int( (xx + winW)*crp  ), int( (yy + winH) * crp  )), (255, 0, 0), 2)

cv2.imwrite('found.png', image)

cv2.imshow("Buldum", image)
cv2.waitKey(1)
time.sleep(100000)