from PIL import Image
import os
import numpy as np

img_list = os.listdir()

for im in img_list:
	if 'img' in im:
		img_array = np.array(Image.open(im))
		img_array[img_array==255] = 1
		img_array[img_array==0] = 255
		img_array[img_array==1] = 0
		p = Image.fromarray(img_array)
		p.save(im)
