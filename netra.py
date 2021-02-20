import cv2
import time
from datetime import datetime, timedelta

eye = cv2.VideoCapture(0)
snap_number = 0
t_start = datetime.now()
t_start_span = datetime.now()
t_interval_seconds = 6
t_span_seconds = 300
snap_set_size = 9
repo = "./snaps/"

while True:
    t_now = datetime.now()
    t_elapsed = t_now - t_start
    t_elapsed_span = t_now - t_start_span
    if t_elapsed.seconds > t_interval_seconds:
        snap_number += 1
        print(snap_number)
        flag, frame = eye.read()
        if not flag:
            print("Got no webcam access. Quitting..")
            break
        else:
            name = repo + "snap_{}.png".format(snap_number)
            cv2.imwrite(name, frame) 
            t_start = datetime.now()
    if snap_number > snap_set_size:
        snap_number = 0
    if t_elapsed_span.seconds > t_span_seconds:
        break
 
eye.release()
cv2.destroyAllWindows()