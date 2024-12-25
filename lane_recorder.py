import time
import csv
import win32gui, win32api
import os
import re
import sys
import PIL
import glob
from PIL import Image
import mss
import pygame


if not (len(sys.argv) > 1):
	print('\nNo save path given!\n=>data_recorder.py <save-path>')
	sys.exit(0)
else:
	save_path=sys.argv[1] + '/'

max_samples=450000
samples_per_second=5

if not os.path.exists(save_path):
    os.makedirs(save_path)


print('Recording starts in 5 seconds...')
time.sleep(5)
print('Recording started!')

current_sample = max([int(re.findall(r'\d+',l)[0]) for l in glob.glob(os.path.join('data', 'img*.bmp'))]) + 1

last_time=0
start_time=time.time()
wait_time=(1/samples_per_second)
stats_frame=0


sct = mss.mss()
mon = {'top': 0, 'left': 0, 'width': 800, 'height': 600}

pause=False
return_was_down=False


while True:
	time.sleep(1.00)
	if (win32api.GetAsyncKeyState(0x24)&0x8001 > 0):
			break

	if (win32api.GetAsyncKeyState(0x0D)&0x8001 > 0):
		if (return_was_down == False):
			if (pause == False):
				pause = True
			else:
				pause = False
				
		return_was_down = True
	else:
		return_was_down = False

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
		
		sct_img = sct.grab(mon)
		img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
		img = img.resize((640, 360), PIL.Image.BICUBIC)
		img = img.crop(box=(0, 150, 640, 360))
		
					
		path = save_path + 'img%d.bmp' % current_sample

		img.save(path, 'BMP')

		current_sample += 1
		
		if (current_sample >= max_samples):
			break
	
	
print('\nDONE')
print('Total Samples: %d\n' % current_sample)
