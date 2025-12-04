import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cv2.namedWindow("Tuner")

def nothing(x): pass

# Trackbars for HSV tuning
cv2.createTrackbar("LH","Tuner",0,179,nothing)
cv2.createTrackbar("LS","Tuner",0,255,nothing)
cv2.createTrackbar("LV","Tuner",0,255,nothing)
cv2.createTrackbar("UH","Tuner",179,179,nothing)
cv2.createTrackbar("US","Tuner",255,255,nothing)
cv2.createTrackbar("UV","Tuner",255,255,nothing)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lh = cv2.getTrackbarPos("LH", "Tuner")
    ls = cv2.getTrackbarPos("LS", "Tuner")
    lv = cv2.getTrackbarPos("LV", "Tuner")
    uh = cv2.getTrackbarPos("UH", "Tuner")
    us = cv2.getTrackbarPos("US", "Tuner")
    uv = cv2.getTrackbarPos("UV", "Tuner")

    lower = np.array([lh, ls, lv])
    upper = np.array([uh, us, uv])

    mask = cv2.inRange(hsv, lower, upper)

    cv2.imshow("Mask", mask)
    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("HSV LOWER =", lower)
        print("HSV UPPER =", upper)
        break

cap.release()
cv2.destroyAllWindows()
