import cv2
import numpy as np
import matplotlib.pyplot as plt

# return sorted list
def ndarray_to_list(convert):
    values = []
    for i in convert:
        values.append(i)
    return sorted(values, key=int, reverse=True)

# First condition => return sum of numbers in 2 lists
def check_point(a, b):
    return (a + b)

# Second condition => return true
def isSafe(h, v):
    return (h > 0 and v > 0)

# Terminate condition => return sum of list
def stop_point(v, h):
    return (sum(v) + sum(h))

def placing_ones(verValues, horValues, img):

    play_yard = np.zeros((width,height), np.uint8)

    if(stop_point(verValues, horValues) == 0):
        return False
    
    i = 0;
    for row in play_yard:
        j = 0;
        for column in row:
            if check_point(horValues[i], verValues[j]) != 0:

                if (isSafe(horValues[i], verValues[j])):

                    play_yard[i][j] = 1
                    verValues[j] -= 1
                    horValues[i] -= 1

                else:
                    play_yard[i][j-1] = 0
                    verValues[j-1] += 1
                    horValues[i] += 1
                    placing_ones(verValues, horValues)

            j += 1
        i += 1

    imgplot = plt.imshow(play_yard)
    plt.show()
    print(play_yard.tolist())
    print(verValues)
    print(horValues)


img = cv2.imread('sample.jpg', cv2.IMREAD_GRAYSCALE)
thresh = 128
im_bw = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]
threshold = 254
im_bw[im_bw<threshold] = 0
im_bw[im_bw>=threshold] = 1
im_bw = 1 - im_bw

imgplot = plt.imshow(img)
plt.show()
print(img)

width = img.shape[0]
height = img.shape[1]

verValues = []
horValues = []

if (width > height):
    vert_original = np.sum(im_bw, axis=0)
    verValues = ndarray_to_list(vert_original)
    print(verValues)
    hor_original = np.sum(im_bw, axis=1)
    horValues = ndarray_to_list(hor_original)
    print(horValues)
else:
    vert_original = np.sum(im_bw, axis=1)
    verValues = ndarray_to_list(vert_original)
    print(verValues)

    hor_original = np.sum(im_bw, axis=0)
    horValues = ndarray_to_list(hor_original)
    print(horValues)

if (sum(horValues) == sum(verValues)):
    placing_ones(verValues, horValues, img)
else: 
    print("this image is not solvable by this method")