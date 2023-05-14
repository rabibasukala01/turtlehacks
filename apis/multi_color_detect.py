# importing required libraries
import cv2
from PIL import Image
from color_detect_util import get_limits
import numpy as np


yellow = [0,255,255] # yellow in BGR
blue = [255,0,0] # blue in BGR
silver = [120,120,120] # grey in BGR
green = [0,255,0] # green in BGR
text_g = "Organic"
text_b = "Recylce"
text_s = "Garbage"
font = cv2.FONT_HERSHEY_SIMPLEX

cap = cv2.VideoCapture(0)

while True:
	ret, frame = cap.read()

	hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	lowerLimit_b, upperLimit_b = get_limits(color=blue)
	lowerLimit_g, upperLimit_g = get_limits(color=green)
	s = np.uint8([[silver]])
	hsvS = cv2.cvtColor(s, cv2.COLOR_BGR2HSV)
	hue_lower = hsvS[0][0][0] - 150
	hue_upper = hsvS[0][0][0] + 150
	if hue_lower < 0:
		hue_lower = 0
	if hue_upper > 179:
		hue_upper = 179
	gray_lower = hue_upper, 0, 0
	gray_upper = hue_upper, 255, 255
	lowerLimit_s = np.array(gray_lower, dtype=np.uint8)
	upperLimit_s = np.array(gray_upper, dtype=np.uint8)
	

	mask_b = cv2.inRange(hsvImage, lowerLimit_b, upperLimit_b)
	mask_g = cv2.inRange(hsvImage, lowerLimit_g, upperLimit_g)
	mask_s = cv2.inRange(hsvImage, lowerLimit_s, upperLimit_s)

	mask__b = Image.fromarray(mask_b)
	mask__g = Image.fromarray(mask_g)
	mask__s = Image.fromarray(mask_s)

	bbox_b = mask__b.getbbox()
	bbox_g = mask__g.getbbox()
	bbox_s = mask__s.getbbox()
	

	if bbox_b is not None:
		x1, y1, x2, y2 = bbox_b

		frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 3) #BGR color
		cv2.putText(frame,text_b,((x1+x2)//2,(y1+y2)//2), font, 1,(0,0,0),2)

	print(bbox_b)
	
	
	if bbox_g is not None:
		x1, y1, x2, y2 = bbox_g

		frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
		cv2.putText(frame,text_g,((x1+x2)//2,(y1+y2)//2), font, 1,(0,0,0),2)

	print(bbox_g)
	

	if bbox_s is not None:
		x1, y1, x2, y2 = bbox_s

		frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (100, 100, 100), 3)
		cv2.putText(frame,text_s,((x1+x2)//2,(y1+y2)//2), font, 1,(0,0,0),2)

	print(bbox_s)
	
    


	cv2.imshow('frame', frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
    
cap.release()

cv2.destroyAllWindows()