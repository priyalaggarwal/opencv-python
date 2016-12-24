import cv2
import imutils

camera = cv2.VideoCapture(0)
lowerColor = (110,50,50)
upperColor = (130,255,255)

left = 350
right = 380

flag=None
prevX=None
prevY=None
x=350
y=380
	

CV_FILLED = -1

while True:
	_, frame = camera.read()
	frame = imutils.resize(frame, 600)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	mask = cv2.inRange(hsv, lowerColor, upperColor)
	mask = cv2.erode(mask, None, iterations=1)
	mask = cv2.dilate(mask, None, iterations=1)

	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]

	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius > 10:
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), CV_FILLED)

		if flag==None:
			prevX=x
			prevY=y
			flag=True
		else:
			if x<prevX:
				left += (prevX-x)
				right += (prevX-x)
			else:
				left -= (x-prevX)
				right -= (x-prevX)

	prevX=x
	prevY=y 			

	# if car goes out of window
	# similar check for right
	if left<0:
		left=0
	if right<0:
		right=30

	cv2.rectangle(frame,(int(left), 350), (int(right), 400),(0,0,0), CV_FILLED)

	cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break