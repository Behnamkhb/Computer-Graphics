import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import itertools
from collections import Counter

# y = mx + b
# r = x.cos(theta) + y.sin(theta)
# point to present => (r, theta)
# where {\displaystyle r} r is the distance from the origin to the closest
# point on the straight line, and theta is the angle between the x axis and
# the line connecting the origin with that closest point.

# calculating theta
# Get distance between two points:
# LENGTH = sqrt[(X1 - X2)^2 + (Y1 - Y2)^2]
# Then get angle: ANGLE = cos^-1[(X2-X1)/LENGTH]
# If Y1 > Y2 then 
# ANGLE = 2PI - ANGLE
# where 2PI is 360 degrees
# D = |cos(theta)(x1-x0) + sin(theta)(y1-y0)|

def set_key(dictionary, key, value):
	if key not in dictionary:
		dictionary[key] = value
	elif type(dictionary[key]) == list:
		dictionary[key].append(value)
	else:
		dictionary[key] = [dictionary[key], value]

img = cv2.imread("lines.jpg", cv2.IMREAD_GRAYSCALE)
img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]
image = (img>0).astype(np.int8)

cv2.imshow("original image", img)
cv2.waitKey(0)

height, width = image.shape
center = [int(width/2), int(height/2)]

valuesX = []
valuesY = []
degrees = []
pair = []
all_rhos = []

x = 0; # coordinates of original
rowCount = 0; m = 0; b = 0;
thetas = list(range(360))

# calculating angel and distance from origin to the current pixel
for row in img:
	colCount = 0
	y = 0
	for col in row:
		if (rowCount < width and colCount < height):
			if (col == 0):
				rhos = []
				for theta in thetas:
					rho = round(abs(math.cos(np.deg2rad(theta)) * y + math.sin(np.deg2rad(theta)) * x))
					rhos.append(rho)

				all_rhos.append(rhos)
			y += 1
		colCount += 1
	rowCount += 1
	x += 1

all_rhos = np.array(all_rhos)

# Calculate the most the common points passing same line
max_repeated = 0
max_theta = 0
max_rho = 0
counter = 0
for i in thetas:
	co = Counter(all_rhos[:,i])
	rho = co.most_common(1)[0][0]
	repeated = co.most_common(1)[0][1]
	if repeated > max_repeated:
		max_theta = i
		max_rho = rho
		max_repeated = repeated

		if max_theta != 0:
			fig = plt.figure()
			ax = plt.axes()
			y0 = int(round(abs((np.cos(np.deg2rad(max_theta)) * 0 - max_rho)/ np.sin(np.deg2rad(max_theta)))))
			y1 = int(round(abs((np.cos(np.deg2rad(max_theta)) * width - max_rho)/ np.sin(np.deg2rad(max_theta)))))
			cv2.line(img, (0, y0), (width, y1), (1,0,0), 2)	
			name = "image" + str(counter) + ".jpg"
			cv2.imwrite(name, img)
			counter += 1
		
print("Maximum number of rhos: " + str(max_rho))
print("Maximum Theta is: " + str(max_theta))

fig = plt.figure()
ax = plt.axes()
y0 = int(round(abs((np.cos(np.deg2rad(max_theta)) * 0 - max_rho)/ np.sin(np.deg2rad(max_theta)))))
y1 = int(round(abs((np.cos(np.deg2rad(max_theta)) * width - max_rho)/ np.sin(np.deg2rad(max_theta)))))
print("Coordinate of Y0: "+ str(y0))
print("Coordinate of Y1: "+ str(y1))
color=(255,0,0)
thickness = 2
cv2.line(img, (0,y0), (width, y1), color, thickness)
cv2.imshow("line with the most pixels include", img)
cv2.waitKey(0)