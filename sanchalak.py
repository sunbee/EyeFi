import watchdog.events
import watchdog.observers
import time
import os
from datetime import datetime

#import dhyana
import parayana



class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        watchdog.events.PatternMatchingEventHandler.__init__(self, 
            patterns=['*.png', '*.jpeg'],
            ignore_directories=True,
            case_sensitive=True
        )
        self.verified = None

    def on_created(self, event):
        print(f"Got new snap {event.src_path}.")

    def on_modified(self, event):
        snap = event.src_path
        print(f"Modified snap {snap}.")
        sense = pX.sense_presence(snap=snap)
        # Check consensus
        if len(list(filter(lambda x: x < 0.005, sense))) > 0:
            toc = datetime.now()
            print(f"{toc} Possible intrusion! Got: {sense}. Verifying..")
            if not self.verified or (toc-self.verified).seconds > 300:        
                snap_object = parayana.Snap(repo=repo, name=os.path.basename(snap))
                PAI.call_vision_api(snap=snap_object)
                out = snap_object.mark_person()
                if out:
                    self.verified = datetime.now()  
                    print(f"{toc} Intruder alert! Intruder alert!")
                    snap_object.send_notification(message="Intruder alert!")
                else:
                    print(f"{toc} Detected no presence. False alarm.")
            else:
                print(f"{toc} Presence verified minutes ago.")
        """
        items = dhyana.detect_objects(snap)
        people = list(filter(lambda item: item.name == "Person", items))
        if len(people) > 0:
            snap_alert = dhyana.mark_person(snap, people[0])
            dhyana.send_notification(snap_alert, "Intrusion detected.")
        """

if os.environ.get('BOT'):
    repo = "/app/snaps"
    BOT = os.environ.get('BOT')
else:
    repo = os.path.expanduser('~/Desktop/Snaps')
    BOT = "Sanjinator"

pX = parayana.PresenceX(repo)
PAI = parayana.PresenceAI()
event_handler = Handler()
observer = watchdog.observers.Observer()

observer.schedule(event_handler, path=repo, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()