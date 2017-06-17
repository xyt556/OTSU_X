"""
Otsu thresholding
==================

This example illustrates automatic Otsu thresholding.
"""

import matplotlib.pyplot as plt
from skimage import data
try:
    from skimage import filters
except ImportError:
    from skimage import filter as filters
from skimage import exposure

import numpy as np
import gdal
from skimage import io, exposure, img_as_uint, img_as_float

ds = gdal.Open("./LC8__IBI.dat")
camera = np.array(ds.GetRasterBand(1).ReadAsArray())

camera2 = camera.flatten()
camera2 = [i for i in camera2 if (i>=-1 and i<=1)]
camera2 = np.asarray(camera2)

val = filters.threshold_otsu(camera2)
print (val)
hist, bins_center = exposure.histogram(camera2)

plt.figure(figsize=(9, 4))
plt.subplot(131)
plt.imshow(camera, cmap='gray', interpolation='nearest')
plt.axis('off')
plt.subplot(132)

camera[camera<val]=np.nan
im = exposure.rescale_intensity(camera, out_range='float')
im = img_as_float(im)
io.imsave('output.png', im)

#plt.imshow(camera < val, cmap='gray', interpolation='nearest')
plt.imshow(camera, cmap='gray', interpolation='nearest')
plt.axis('off')
plt.subplot(133)

plt.plot(bins_center, hist, lw=2)
plt.axvline(val, color='k', ls='--')

plt.tight_layout()
plt.show()
