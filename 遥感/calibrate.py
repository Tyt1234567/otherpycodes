import numpy as np
import rasterio
from generate_cofficients import bands_k, bands_b

samples = 2400
lines   = 1500

with rasterio.open(r'D:\遥感实习数据\20240623\aosen_resize') as img:
    bands_dataset = []
    for i in range(1,img.count+1):
        band = img.read(i).astype(np.float32)
        bands_dataset.append(band)

for i,band in enumerate(bands_dataset):
    for line in range(lines):
        for row in range(samples):
            band[line][row] = band[line][row]*bands_k[i] + bands_b[i]

print(bands_dataset)

with open(r'D:\遥感实习数据\20240623\calibrate','wb') as f:
    for band in bands_dataset:
        band.tofile(f)
