import cv2
# import picamera
import time
from datetime import datetime, timedelta
import os

class netraMAC:
    def __init__(self, repo, size=9, interval=6, span=600, baseline=3):
        """
        Constructor with args as follows:
        repo (string) is the path to the local stash for snaps.
        snaps_set_size (int) is the number of snaps in the collection.
        interval (int) is the number of seconds between successive snaps.
        span (int) is the length of time (in seconds) before program quits.
        """
        self.repo = repo
        self.size = size
        self.interval = interval
        self.span = span
        self.baseline = baseline

    def activate(self):
        eye = cv2.VideoCapture(0)
        snap_number = 0
        t_start = datetime.now()
        t_start_span = datetime.now()
        t_interval_seconds = self.interval
        t_span_seconds = self.span
        snap_set_size = self.size
        repo = os.path.expanduser(self.repo) # "~/Desktop/Snaps/"
      
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
                    if self.baseline:
                        name = os.path.join(repo, "baseline_{}.png".format(snap_number))
                        self.baseline -= 1
                    else:
                        name = os.path.join(repo, "snap_{}.png".format(snap_number))
                    print(name)
                    frame_timestamped = cv2.putText(frame, 
                                        text=t_now.strftime('%d %B, %Y %H:%M:%S'), 
                                        org=(51, 51), 
                                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                                        fontScale=1.2, 
                                        color=(0, 0, 0), 
                                        thickness=2)
                    cv2.imwrite(name, frame_timestamped)
                    t_start = datetime.now()
            if snap_number > snap_set_size:
                snap_number = 0
            if t_elapsed_span.seconds > t_span_seconds:
                break
        
        eye.release()
        cv2.destroyAllWindows()
        
