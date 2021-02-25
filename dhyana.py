from google.cloud import vision
import requests
from cv2 import *
import config
import os
import base64

def detect_objects(snap):
    """
    Detect objects in the snap using Google Cloud Vision.
    args:
        snap: (string) Give the full path to the snap on local drive.
    return:
        List containing annotation objects with detection label and likelihood informaation.
    Notes:
        path = os.path.expanduser('~/Desktop/Snaps')
        snap = os.path.join(path, 'snap_1.png')
    """
    client = vision.ImageAnnotatorClient()
    print(snap)

    with open(snap, 'rb') as im_file:
        content = im_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(image=image).localized_object_annotations

    print(f"Found {len(objects)} objects")
    [print(f"{objet.name} : {round(objet.score*100,2)}") for objet in objects]
    
    return objects

def detect_person(snap):
    """
    Detect the presence of a person in the snap using Google Cloud Vision.
    """
    pass

def mark_person(snap, annot, switch_format=True):
    """
    Mark the person or persons in the image.
    Use this command when a person is detected in the snap,
    with the image object for manipulation in opencv.
    args:
        frame: (image object in opencv) the input to process
        annot: (annotation object from Google Cloud Vision client) the annotation
    """
    frame = cv2.imread(snap)
    height, width, _ = frame.shape

    iTL = 0
    iBR = 2
    TL = (int(annot.bounding_poly.normalized_vertices[iTL].x * width),
        int(annot.bounding_poly.normalized_vertices[iTL].y * height))
    BR = (int(annot.bounding_poly.normalized_vertices[iBR].x * width),
        int(annot.bounding_poly.normalized_vertices[iBR].y * height))
    
    print(f"Drawing from {TL} to {BR}")

    color = (0, 0, 255)
    thickness = 2
    frame = cv2.rectangle(frame, TL, BR, color, thickness)
    if switch_format:
        snap = snap.replace("png", "jpeg")
    cv2.imwrite(snap, frame)
    return snap

def send_notification(snap, message):
    """
    Send a push notification to the subscriber
    containing the snap with the person marked
    and a message identifying the sender (e.g. bot).
    The subscriber can then use Telegram 
    to get the surveillance footage.
    """
    snapb64 = encodeSnapBase64(snap)
    push_notification("Alert!", "Intrusion Alert!", snapb64)
    pass


def encodeSnapBase64(snap):
    with open(snap, 'rb') as img:
        return ", ".join(('data:image/jpeg;base64', base64.b64encode(img.read()).decode('utf-8')))

def push_notification(title, message, picture=""):
    packet = {
        "k": config.pushkey,    # API key
        "m": message,           # message
        "t": title,             # title
        "i": "98",              # icon no.  1-98
        "s": "28",              # sound no. 0-28
        "v": "3",               # vibr mode 0-3
        "p": picture
    }
    r = requests.post("https://pushsafer.com:443/api", data=packet)