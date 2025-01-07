import os
import cv2
import mss
import time
import torch
import pygame
import numpy as np
from PIL import Image
from model import UNET
import albumentations as A
from albumentations.pytorch import ToTensorV2
from utils import (
		load_checkpoint,
		save_checkpoint,
		get_loaders,
		check_accuracy,
		save_predictions_as_imgs
	)

pygame.init()
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("GTAV constructed image")
clock = pygame.time.Clock()

IMAGE_HEIGHT = 160
IMAGE_WIDTH = 240
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

sct = mss.mss()
mon = {'top': 0, 'left': 0, 'width': 800, 'height': 600}
pause=False
last_time=0
start_time=time.time()
max_samples=450000
samples_per_second=30
current_sample = 0
stats_frame=0
wait_time=(1/samples_per_second)

model = UNET(in_channels=3, out_channels=1).to(DEVICE)
checkpoint = torch.load('my_checkpoint.pth.tar')
model.load_state_dict(checkpoint['state_dict'])
model.eval()
transform = A.Compose(
		[
			A.Resize(height=IMAGE_HEIGHT, width=IMAGE_WIDTH),
			A.Normalize(
					mean=[0.0, 0.0, 0.0],
					std=[1.0, 1.0, 1.0],
					max_pixel_value=255.0
				),
			ToTensorV2()
		]
	)

while True:
	if (time.time() - last_time >= wait_time):
	
		fps=1 / (time.time() - last_time)
		last_time = time.time()
		
		stats_frame+=1
		if (stats_frame >= 10):
			stats_frame=0
			os.system('cls')
			print('FPS: %.2f Total Samples: %d Time: %s' % (fps, current_sample, time.strftime("%H:%M:%S",time.gmtime(time.time() - start_time))))
			if (pause == False):
				print('Status: Recording')
			else:
				print('Status: Paused')
		
		if (pause):
			time.sleep(0.01)
			continue
		
		start_time = time.time()
		sct_img = sct.grab(mon)
		print("Frame Capture Time: ", time.time() - start_time)
		img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
		img = img.resize((640, 360), Image.BICUBIC)
		org_img = img
		org_img = np.array(org_img)

		x_start, y_start = 5, 290
		x_end, y_end = 130, 360

		original_values = org_img[y_start:y_end, x_start:x_end, :].copy()
		org_img = org_img / 4

		org_img[y_start:y_end, x_start:x_end, :] = original_values


		img = img.crop(box=(0, 150, 640, 360))
		img_np = np.array(img)

		transformed = transform(image=img_np)
		input_tensor = transformed['image'] 

		input_tensor = input_tensor.unsqueeze(0) 
		input_tensor = input_tensor.to(DEVICE)

		start_time = time.time()
		preds = torch.sigmoid(model(input_tensor))
		print("Inference Time: ", time.time() - start_time)
		preds = (preds > 0.5).float()

		mask_np = preds.squeeze().cpu().numpy()
		start_time = time.time()
		resized_mask = cv2.resize(mask_np, (640, 210), interpolation=cv2.INTER_NEAREST)
		print("Mask Resize Time: ", time.time() - start_time)

		mask = resized_mask == 1

		start_time = time.time()
		org_img[150:150 + mask.shape[0], :, 0] = np.where(mask, 0, org_img[150:150 + mask.shape[0], :, 0])
		org_img[150:150 + mask.shape[0], :, 1] = np.where(mask, 255, org_img[150:150 + mask.shape[0], :, 1])
		org_img[150:150 + mask.shape[0], :, 2] = np.where(mask, 0, org_img[150:150 + mask.shape[0], :, 2])

		print("Apply mask time: ", time.time() - start_time)

		image_array = np.transpose(org_img, (1, 0, 2))

		resized_array = cv2.resize(image_array, (600, 800))
		image_surface = pygame.surfarray.make_surface(resized_array)

		screen.fill((0, 0, 0))
		screen.blit(image_surface, (0, 0)) 
		pygame.display.update()

		clock.tick(30)
		current_sample += 1

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

		if (current_sample >= max_samples):
			break

	