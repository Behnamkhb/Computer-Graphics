import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

im = Image.open('img.png')
width, height = im.size

# Dilation
def dilationImage():
	img = cv2.imread('img.png', cv2.IMREAD_GRAYSCALE)
	img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)[1]
	img = 255 - img

	positionCheckerRow = 0
	dilation = []

	for row in img:
		positionCheckerColumn = 0
		row_ = row.copy()

		# it should not modify orginal row
		# at the end of each row, it should replace final result of row same with orginal one

		# row 0
		while (positionCheckerRow == 0 and positionCheckerColumn < width - 1):  
			if (positionCheckerColumn == 0):
				if (row[positionCheckerColumn + 1] == 255 or img[positionCheckerRow + 1][positionCheckerColumn] == 255):
					row_[positionCheckerColumn] = 255

			elif (positionCheckerColumn < height - 1 or positionCheckerColumn < width - 1):
				if (row[positionCheckerColumn - 1] == 255 or 
					row[positionCheckerColumn + 1] == 255 or 
					img[positionCheckerRow + 1][positionCheckerColumn] == 255):
					row_[positionCheckerColumn] = 255

			elif (positionCheckerColumn == width - 1):
				if (row[positionCheckerColumn - 1] == 255 or img[positionCheckerRow + 1][positionCheckerColumn] == 255):
					row_[positionCheckerColumn] = 255

			positionCheckerColumn += 1

		# Middle pixels
		while (((positionCheckerRow > 0 and positionCheckerRow < width - 1) or
				(positionCheckerRow > 0 and positionCheckerRow < height - 1)) and
				positionCheckerColumn < width):

			if (positionCheckerColumn == 0):
				if (row[positionCheckerColumn + 1] == 255 or 
					img[positionCheckerRow - 1][positionCheckerColumn] == 255 or
					img[positionCheckerRow + 1][positionCheckerColumn] == 255):
					row_[positionCheckerColumn] = 255

			elif (positionCheckerColumn < width - 1 or positionCheckerColumn < height - 1):
				if (row[positionCheckerColumn - 1] == 255 or row[positionCheckerColumn + 1] == 255 or 
					img[positionCheckerRow - 1][positionCheckerColumn] == 255 or img[positionCheckerRow + 1][positionCheckerColumn] == 255):
					row_[positionCheckerColumn] = 255

			elif (positionCheckerColumn == width - 1):
				if (row[positionCheckerColumn - 1] == 255 or 
					img[positionCheckerRow - 1][positionCheckerColumn] == 255 or 
					img[positionCheckerRow + 1][positionCheckerColumn] == 255):
					row_[positionCheckerColumn] = 255

			positionCheckerColumn += 1

		# row 50
		while (positionCheckerRow == height - 1 and positionCheckerColumn < width - 1):
			if (positionCheckerColumn == 0):
				if (row[positionCheckerColumn + 1] == 255 or img[positionCheckerRow - 1][positionCheckerColumn] == 255):
					row_[positionCheckerColumn] = 255

			elif (positionCheckerColumn < height - 1 or positionCheckerColumn < width - 1):
				if (row[positionCheckerColumn - 1] == 255 or 
					row[positionCheckerColumn + 1] == 255 or 
					img[positionCheckerRow - 1][positionCheckerColumn] == 255):
					row_[positionCheckerColumn] = 255

			elif (positionCheckerColumn == width - 1):
				if (row[positionCheckerColumn - 1] == 255 or img[positionCheckerRow - 1][positionCheckerColumn] == 255):
					row_[positionCheckerColumn] = 255

			positionCheckerColumn += 1

		dilation.append(row_)
		positionCheckerRow += 1

	array = np.array(dilation, dtype=np.uint8)
	diation_image = Image.fromarray(array)
	res1 = np.hstack((img, diation_image))
	return res1

# Erosion
def erosionImage():
	img = cv2.imread('img.png', cv2.IMREAD_GRAYSCALE)
	img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)[1]
	img = 255 - img

	positionCheckerRow = 0
	erosion = []

	# all values should be 255 otherwise put 0
	for row in img:
		positionCheckerColumn = 0
		row_ = row.copy()

		while (positionCheckerColumn < width - 1):
			if (row[positionCheckerColumn] == 255):

				if (row[positionCheckerColumn + 1] != None and
					row[positionCheckerColumn - 1] != None and
					img[positionCheckerRow - 1][positionCheckerColumn] != None and
					img[positionCheckerRow + 1][positionCheckerColumn] != None):

					if (row[positionCheckerColumn + 1] == 255 and
						row[positionCheckerColumn - 1] == 255 and
						img[positionCheckerRow - 1][positionCheckerColumn] == 255 and
						img[positionCheckerRow + 1][positionCheckerColumn] == 255):
						row_[positionCheckerColumn] = 255
						positionCheckerColumn += 1 
					else:
						row_[positionCheckerColumn] = 0
						positionCheckerColumn += 1 
			else:
				row_[positionCheckerColumn] = 0
				positionCheckerColumn += 1
		positionCheckerRow += 1

		erosion.append(row_)

	array = np.array(erosion, dtype=np.uint8)
	erosion_image = Image.fromarray(array)
	res2 = np.hstack((dilationImage(), erosion_image))
	cv2.imwrite('sample_image.png', res2)
	plt.figure()
	plt.imshow(res2, cmap='gray');
	plt.show()

erosionImage()