import cv2
bg=cv2.VideoCapture(0)
while True:
    ret,frame=bg.read()
    cv2.imshow("",frame)