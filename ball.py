
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import sys
PY3 = sys.version_info[0] == 3
if PY3:
	xrange = range
# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

camera = cv2.VideoCapture(0)
pts = deque(maxlen=64)
# keep looping
def getit(_width,_height) :
	# grab the current frame
	camera = cv2.VideoCapture(0)
	(grabbed, frame) = camera.read()
 # resize the frame, blur it, and convert it to the HSV color space
	frame = imutils.resize(frame, width=_width,height=_height)
	frame = cv2.flip(frame,1)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	# find contours in the mask and initialize the current (x, y) center of the color mass
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
 
	# update the points queue
	pts.appendleft(center)
	# loop over the set of tracked points
	for i in xrange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), 4)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		return 0
	camera.release()
	return(frame,center) 
"""
	# show the frame to our screen
	cv2.namedWindow("base-image", cv2.WINDOW_AUTOSIZE)  
	cv2.namedWindow("result-image", cv2.WINDOW_AUTOSIZE)

	#Position the windows next to eachother
	cv2.moveWindow("base-image",0,100)  
	cv2.moveWindow("result-image",600,100)

	#Start the window thread for the two windows we are using
	cv2.startWindowThread()

	cv2.imshow("base-image", frame)
	
	cv2.imshow("result-image", mask)
	"""
	
 
	# if the 'q' key is pressed, stop the loop
# cleanup the camera and close any open windows

#cv2.destroyAllWindows()
