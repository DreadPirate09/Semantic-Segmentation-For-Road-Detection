from PIL import Image
import numpy as np
import os

imgs = os.listdir()

for i,im in enumerate(imgs):
	if "_mask.bmp" in im:
		img = Image.open(im)
		img = np.array(img)
		mask = np.any(img != [0,0,0], axis=-1)
		img[mask] = [255,255,255]
		processed_image = Image.fromarray(img)
		processed_image.save(im.replace("_mask",""))
		os.remove(im)