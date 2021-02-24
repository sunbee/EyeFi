import watchdog.events
import watchdog.observers
import time
import os

import dhyana

class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        watchdog.events.PatternMatchingEventHandler.__init__(self, 
            patterns=['*.png'],
            ignore_directories=True,
            case_sensitive=True
        )

    def on_created(self, event):
        print(f"Got new snap {event.src_path}.")

    def on_modified(self, event):
        snap = event.src_path
        print(f"Modified snap {snap}.")
        items = dhyana.detect_objects(snap)
        people = list(filter(lambda item: item.name == "Person", items))
        if len(people) > 0:
            dhyana.mark_person(snap, people[0])

    
repo = os.path.expanduser('~/Desktop/Snaps')
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