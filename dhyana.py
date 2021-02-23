from google.cloud import vision
from cv2 import *
import os

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

def mark_person(snap, annot):
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
    cv2.imwrite(snap, frame)

def send_notification(snap, message):
    """
    Send a push notification to the subscriber
    containing the snap with the person marked
    and a message identifying the sender (e.g. bot).
    The subscriber can then use Telegram 
    to get the surveillance footage.
    """
    pass



