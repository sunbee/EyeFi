from google.cloud import vision
import os


client = vision.ImageAnnotatorClient()
path = os.path.expanduser('~/Desktop/Snaps')
snap = os.path.join(path, 'snap_1.png')
print(snap)

with open(snap, 'rb') as im_file:
    content = im_file.read()
image = vision.Image(content=content)

objects = client.object_localization(image=image).localized_object_annotations

print(f"Found {len(objects)} objects")
[print(f"{objet.name} : {round(objet.score*100,2)}") for objet in objects]