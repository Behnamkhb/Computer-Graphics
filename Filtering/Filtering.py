import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('sample.jpg', cv2.IMREAD_GRAYSCALE)
height = img.shape[0]
width = img.shape[1]
centerX = int(width/2)
centerY = int(height/2)

# should calculate center
center = img[int(width/2), int(height/2)]

# F(x, y)
f = np.fft.fft2(img)

# we want to concentrate all high frequesncy to the center: we use shift bellow
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20*np.log(np.abs(fshift))
magnitude_spectrum = np.asarray(magnitude_spectrum, dtype=np.uint8)
magnitude_spectrum_ = np.concatenate((img, magnitude_spectrum), axis=1)
h = magnitude_spectrum.shape

# Circular Mask
CIRCLE_RADIUS = 10
CIRCLE_THICKNESS = -1

# symmetric filter function H(u,v) Ideal low Pass Filter
IHPF_filter = np.ones_like(img, dtype='uint8')*1
Highcir = np.array(cv2.circle(IHPF_filter, (centerX, centerY), CIRCLE_RADIUS, 0, CIRCLE_THICKNESS))
ILPF_filter = np.zeros_like(img, dtype='uint8')
Lowcir = np.array(cv2.circle(ILPF_filter, (centerX, centerY), CIRCLE_RADIUS, 1, CIRCLE_THICKNESS))

# Calculate G(u,v)=F(u,v)H(u,v)
hFunc = fshift * Highcir
lFunc = fshift * Lowcir

img_filter_high = np.asarray(magnitude_spectrum*Highcir, dtype=np.uint8)
magnitude_spectrum_high = np.concatenate((magnitude_spectrum_, img_filter_high), axis=1)

img_filter_low = np.asarray(magnitude_spectrum*Lowcir, dtype=np.uint8)
magnitude_spectrum_low = np.concatenate((magnitude_spectrum_, img_filter_low), axis=1)

# Compute g(x,y) based on inverse Fourier transform
high_f_ishift = np.fft.ifftshift(hFunc)
high_img_back = np.fft.ifft2(high_f_ishift)
high_img_back = np.abs(high_img_back)
high_img_back = np.array(high_img_back, dtype=np.uint8)

low_f_ishift = np.fft.ifftshift(lFunc)
low_img_back = np.fft.ifft2(low_f_ishift)
low_img_back = np.abs(low_img_back)
low_img_back = np.array(low_img_back, dtype=np.uint8)

result_high = np.concatenate((magnitude_spectrum_high, high_img_back), axis=1)
result_low = np.concatenate((magnitude_spectrum_low, low_img_back), axis=1)
cv2.imshow("IHPF", result_high)
cv2.imshow("ILPF", result_low)
cv2.waitKey(0)
cv2.destroyAllWindows()