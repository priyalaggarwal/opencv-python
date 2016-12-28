import cv2

faceCascade = cv2.CascadeClassifier('/home/dell/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('/home/dell/opencv/data/haarcascades/haarcascade_eye.xml')
smileCascade = cv2.CascadeClassifier('/home/dell/opencv/data/haarcascades/haarcascade_smile.xml')

camera = cv2.VideoCapture(0)
camera.set(3,640)
camera.set(3,480)

scaleFactor = 1.05

while True:

    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    roi_gray = None
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor= scaleFactor,
        minNeighbors=8,
        minSize=(55, 55)
    )

    for (x, y, w, h) in faces:
    	roi_gray = gray[y:y+h, x:x+h]
    	roi_color = frame[y:y+h, x:x+h]

    	eyes = eyeCascade.detectMultiScale(roi_gray)

    	if eyes is not None:
    		smiles = smileCascade.detectMultiScale(
	    	roi_gray,
	        scaleFactor= 1.5,
	        minNeighbors=22,
	        minSize=(25, 25)
	    	)
    		for (x, y, w, h) in smiles:
    			cv2.rectangle(roi_color, (x, y), (x+w, y+h), (0, 255, 0), 1)

    cv2.imshow('Smile Detector', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break