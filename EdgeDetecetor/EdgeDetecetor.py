import cv2
import numpy as np
from PIL import Image

img = cv2.imread("image.jpg", cv2.IMREAD_GRAYSCALE)

# f = f(img[j-1][i-1]) + f(img[j-1][i]) + f(img[j-1][i+1])
#   + f(img[j][i-1]) - 8*f(img[j][i]) + f(img[j][i+1])
#   + f(img[j+1][i-1]) + f(img[j+1][i]) + f(img[j+1][i+1])
#  8-neighbothood Laplace operator
# mask = [[1, 1, 1],
#       [1, -8, 1],
#       [1, 1, 1]]
#  4-neighbothood Laplace operator
# mask = [[0, 1, 0],
#       [1, -4, 1],
#       [0, 1, 0]]

height = img.shape[0]
width = img.shape[1]
size = width * height
colPosition = 0
new_image_4 = []
new_image_8 = []
new_image_8_NoInt = []

# 4-neighborhoods
for row in img:
	row_ = row.copy()
	rowPosition = 0
	for pixel in row:
		if (rowPosition < width - 1 and rowPosition > 0 and colPosition < height -1 and colPosition > 0):
			value = abs(int(img[colPosition-1][rowPosition-1]) + int(img[colPosition-1][rowPosition]) + int(img[colPosition-1][rowPosition+1])
			+ int(img[colPosition][rowPosition-1]) - 8*int(img[colPosition][rowPosition]) + int(img[colPosition][rowPosition+1])
			+ int(img[colPosition+1][rowPosition-1]) + int(img[colPosition+1][rowPosition]) + int(img[colPosition+1][rowPosition+1]))
			
			row_[rowPosition] = value
		rowPosition += 1
	colPosition += 1
	new_image_8.append(row_)

# 8-neighborhoods with int values
colPosition = 0
for row in img:
	row_ = row.copy()
	rowPosition = 0
	for pixel in row:
		if (rowPosition < width - 1 and rowPosition > 0 and colPosition < height -1 and colPosition > 0):
			value = abs(0*int(img[colPosition-1][rowPosition-1]) + int(img[colPosition-1][rowPosition]) + 0*int(img[colPosition-1][rowPosition+1])
			+ int(img[colPosition][rowPosition-1]) - 4*int(img[colPosition][rowPosition]) + int(img[colPosition][rowPosition+1])
			+ 0*int(img[colPosition+1][rowPosition-1]) + int(img[colPosition+1][rowPosition]) + 0*int(img[colPosition+1][rowPosition+1]))

			row_[rowPosition] = value
		rowPosition += 1
	colPosition += 1
	new_image_4.append(row_)

new_image = np.array(new_image_8)
new_image_noInt = np.array(new_image_8_NoInt)
new_image_4 = np.array(new_image_4)
cv2.imshow("8-Laplace Transform", new_image)
cv2.imshow("4-Laplace Transform", new_image_4)
cv2.imshow("original image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()