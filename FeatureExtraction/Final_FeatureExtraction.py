import numpy as np
import cv2
import matplotlib.pyplot as plt
import pygame, sys
import pygame
from collections import Counter
import random

img = cv2.imread("U_.jpg", cv2.IMREAD_GRAYSCALE)
thresh = 128
img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]
# img = 255 - img
# print(img.tolist())

width, height = img.shape
size = width * height

values = 1
values1 = 0
values2 = 0
rowCounter = 0
new_image = []
regions = []
equalities = []

for row in img:
    colCounter = 0  
    for pixel in row:
        if (row[colCounter - 1] == 0 and img[rowCounter - 1][colCounter] == 0):
            if (pixel != 0):
                row[colCounter] = values
                values += 1
            regions.append(values)

        elif (row[colCounter - 1] != 0 or img[rowCounter - 1][colCounter] != 0):
            if (pixel != 0):
                if (row[colCounter - 1] != 0 and img[rowCounter - 1][colCounter] == 0):
                    if (str(row[colCounter]) + " : " + str(row[colCounter - 1]) not in equalities):
                        equalities.append(str(row[colCounter]) + " : " + str(row[colCounter - 1]))
                    values1 = row[colCounter - 1]
                    row[colCounter] = values1

                elif (row[colCounter - 1] == 0 and img[rowCounter - 1][colCounter] != 0):
                    if (str(row[colCounter]) + " : " + str(img[rowCounter - 1][colCounter]) not in equalities):
                        equalities.append(str(row[colCounter]) + " : " + str(img[rowCounter - 1][colCounter]))
                    values2 = img[rowCounter - 1][colCounter]
                    row[colCounter] = values2

                elif ((row[colCounter - 1] != 0 and img[rowCounter - 1][colCounter] != 0)):
                    values1 = row[colCounter - 1]
                    row[colCounter] = values1
                    values2 = img[rowCounter - 1][colCounter]
                    row[colCounter] = values2
                    if (values1 > values2):
                        if (str(row[colCounter]) + " : " + str(img[rowCounter - 1][colCounter]) not in equalities):
                            equalities.append(str(row[colCounter]) + " : " + str(img[rowCounter - 1][colCounter]))
                        regions.append(values2)
                    else:
                        if (str(row[colCounter]) + " : " + str(row[colCounter - 1]) not in equalities):
                            equalities.append(str(row[colCounter]) + " : " + str(row[colCounter - 1]))
                        regions.append(values1)

        colCounter += 1
    rowCounter += 1
    new_image.append(row)

# print(regions)
print(new_image)

# FInal Labeling
values = 1
values1 = 0
values2 = 0
rowCounter = 0
final_regions = []
final_extraction = []

new_image = new_image[::-1]
print(new_image)
for row in new_image:
    colCounter = 0  
    for pixel in row:

        if (row[colCounter - 1] != 0 or new_image[rowCounter - 1][colCounter] != 0):
            if (pixel != 0):
                if (row[colCounter - 1] != 0 and new_image[rowCounter - 1][colCounter] == 0):
                    if (row[colCounter - 1] < row[colCounter]):
                        if (str(row[colCounter]) + " : " + str(row[colCounter - 1]) not in equalities):
                            equalities.append(str(row[colCounter]) + " : " + str(row[colCounter - 1]))
                        values1 = row[colCounter - 1]
                        row[colCounter] = values1

                elif (row[colCounter - 1] == 0 and new_image[rowCounter - 1][colCounter] != 0):
                    if (new_image[rowCounter - 1][colCounter] < row[colCounter]):
                        if (str(row[colCounter]) + " : " + str(new_image[rowCounter - 1][colCounter]) not in equalities):
                            equalities.append(str(row[colCounter]) + " : " + str(new_image[rowCounter - 1][colCounter]))
                        values2 = new_image[rowCounter - 1][colCounter]
                        row[colCounter] = values2

                elif ((row[colCounter - 1] != 0 and new_image[rowCounter - 1][colCounter] != 0)):
                    values1 = row[colCounter - 1]
                    row[colCounter] = values1
                    values2 = new_image[rowCounter - 1][colCounter]
                    row[colCounter] = values2
                    if (values1 > values2):
                        if (str(row[colCounter]) + " : " + str(new_image[rowCounter - 1][colCounter]) not in equalities):
                            equalities.append(str(row[colCounter]) + " : " + str(new_image[rowCounter - 1][colCounter]))
                        final_regions.append(values2)
                    else:
                        if (str(row[colCounter]) + " : " + str(row[colCounter - 1]) not in equalities):
                            equalities.append(str(row[colCounter]) + " : " + str(row[colCounter - 1]))
                        final_regions.append(values1)

        colCounter += 1
    rowCounter += 1
    final_extraction.append(row)

# print(final_regions)
final_extraction = final_extraction[::-1]
print(final_extraction)
# Convert final_extraction to 1D array
extra = np.array(final_extraction).ravel()
final_extraction = np.array(final_extraction).tolist()
print(equalities)

# Pygame display
COLORS = {}
matrix_ = []
matrix = [final_extraction[i:i+width] for i in range(0, len(final_extraction), width)]
dic = Counter(extra)
dictionary = dict(dic)

# Convert [[[]]] to [[]]
for i in matrix:
    for j in i: 
        matrix_.append(j)
matrix = matrix_

# Create random colors for each label
COLORS = {}
r = lambda: random.randint(0,255)
for key in dictionary.keys():
	COLORS[key] = (r(),r(),r())
print(COLORS)

MARGIN = 5
TILESIZE = 20
MAPWIDTH = width
MAPHEIGHT = len(matrix)

pygame.init()

DISPLAYSUFRACE = pygame.display.set_mode((int(MAPWIDTH * (TILESIZE + MARGIN)), int(MAPHEIGHT * (TILESIZE + MARGIN))))

while True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	for row in range(MAPHEIGHT):
		for column in range(MAPWIDTH):
			pygame.draw.rect(DISPLAYSUFRACE, COLORS[matrix[row][column]], 
				(column * (MARGIN + TILESIZE), row * (MARGIN + TILESIZE), TILESIZE, TILESIZE))

	pygame.display.update()

pygame.quit()