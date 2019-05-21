import cv2
from matplotlib import pyplot as plt
from collections import Counter

img = cv2.imread('image.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# print(img)
cv2.imshow("image",img)
cv2.waitKey(0)

height = img.shape[ 0]
width = img.shape[1]
size = width * height

previousVale = 0
dicProbability = {}
cumulativeProbability = {}
finalCumulative = dict()
values = img.reshape((size))

# h[g] = h[g] + 1
dictionary = dict(Counter(values))

x = dictionary.values()
y = dictionary.keys()
plot_ = plt.hist([[float(x_) for x_ in x] for y_ in y])
plt.title("Before Equalization Histogram")
plt.xlabel("All Pixels Variable")
plt.ylabel("Pixels")
plt.show()

# calculating cumulative
for key in sorted(dictionary.keys()):
	value = dictionary[key]
	val = value + previousVale
	previousVale = val
	cumulativeProbability[key] = val

# calculating T[p] for each pixel-value
for key in sorted(cumulativeProbability.keys()):
	value = cumulativeProbability[key]
	finalCumulative[key] = round((255 / size) * value)

# g = T[p]
for i in range(height):
	for j in range(width):
		img[i, j] = finalCumulative[img[i, j]]

x = cumulativeProbability.values()
y = cumulativeProbability.keys()
plot_ = plt.hist([[float(x_) for x_ in x] for y_ in y])
plt.title("After Equalization Histogram")
plt.xlabel("All Pixels Variable")
plt.ylabel("Pixels")
plt.show()

cv2.imshow("Equalized", img)
cv2.waitKey(0)