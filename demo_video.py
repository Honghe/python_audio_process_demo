import cv2
import time

host = '172.31.23.142'
stream = '2'

cap = cv2.VideoCapture('rtsp://' + host + '/' + stream)

while True:
    retval, frame = cap.read()

    # Place options to overlay on the video here.
    cv2.imshow(('Camera' + str(host)), frame)
    k = cv2.waitKey(0) & 0xFF
    if k == 27:  # esc key ends process
        cap.release()
        break
cv2.destroyAllWindows()
