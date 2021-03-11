from PIL import Image, ImageFont, ImageDraw
import os
import glob
import numpy as np
import scipy.stats as scs
import base64
import requests
import json
import config

class PresenceX:
    def __init__(self, repo, sample_size=999, scale_factor=3):
        """
        Establish a baseline from repo for presence detection 
        with the set of still images in the specified repository.
        Delegates tp internal methods.
        Args: 
            repo (string) the local folder where snaps are deposited.
            sample_size (int) will be used to sample pixel values from grayscale image.
            scale_factor (int) wull be used to reduce the size of the original image.
        Returns: the baseline (list of numpy arrays) for use by class methods.

        Note: The baseline images must be clearly marked as baseline*.png for use.

        TODO's: 
        1. Check the scale_factor isn't reducing the image size below a threshold.
        2. Add rebase=True flag to continually update baseline based on history.
        3. Since the baseline is a list of arrays, consider a moving average scheme.
        """
        self.repo = repo
        self.sample_size = sample_size
        self.scale_factor = scale_factor
        self.baseline = self._set_baseline()
    
    def _sample_random(self, snap):
        snap_gray = Image.open(snap).convert('L')
        thumbnail_size = (int(snap_gray.size[0]/self.scale_factor), int(snap_gray.size[1]/self.scale_factor))

        return np.random.choice(np.array(Image.open(snap)
                                    .convert('L')
                                    .resize(thumbnail_size))
                                    .flatten(), self.sample_size)

    def _set_baseline(self):
        """
        Set up the baseline from the repo at initialization.
        The repo must contain snaps in PNG format 
        and labeled appropriately.
        This method will then execute steps as follows:
        1. Search for the snaps representative of baseline.
        2. Estimate the scale-factor for size reduction.
        3. For each image: open, convert to grayscale, reduce size, flatten, sample.
        The resulting list of numpy arrays is stored as an object attribute.
        """
        snaps = glob.glob(os.path.join(self.repo, '*.png'))
        snaps_baseline = list(filter(lambda snap: 'baseline' in os.path.basename(snap), snaps))
        if len(snaps_baseline) < 3:
            raise("Found no snaps to establish baseline. Quitting.")
    
        baseline = [self._sample_random(snap) for snap in snaps_baseline]
        return baseline # List of numpy arrays.

    def sense_presence(self, snap):
        """
        """
        canary = self._sample_random(snap)
        return [scs.mannwhitneyu(canary, baseline).pvalue for baseline in self.baseline]

class Snap:
    def __init__(self, repo, name):
        self.repo = repo
        self.name = name
        self.full_name = os.path.join(repo, name)
        self.request = None
        self.response = None

    def _extract_bb(self):
        """
        First, check whether the objects detected in the image include a person.
        Second, get the coordinates of the top-left corner and the bottom-right corner.
        Note that the API reports coordinates relative to the image shape.
        """
        if not self.response:
            return None

        person = list(filter(lambda x: x['name'] == 'Person', self.response.get('responses')[0]['localizedObjectAnnotations']))
        if not person:
            return None

        bb = person[0].get('boundingPoly').get('normalizedVertices')
        tl = (bb[0].get('x'), bb[0].get('y'))
        br = (bb[2].get('x'), bb[2].get('y'))
        print(f"Got bounding box as {tl} and {br} relative to size.")
        return (tl, br)

    def snap_mark(self, box=((0,0), (1, 1))):
        snapJPEG = self.full_name.replace('.png', '.jpeg')
        img_src = Image.open(self.full_name)
        w, h = img_src.size
        tl = (int(box[0][0]*w), int(box[0][1]*h))
        br = (int(box[1][0]*w), int(box[1][1]*h))
        img_drw = ImageDraw.Draw(img_src)
        img_drw.rectangle((tl, br), outline='red', width=6)
        img_src.save(snapJPEG)
        return snapJPEG

    def snap_timestamp(self, message, anchor=(10,10)):
        img_src = Image.open(self.full_name)
        w, h = img_src.size
        img_drw = ImageDraw.Draw(img_src)
        img_fnt = ImageFont.truetype('./Open_Sans/OpenSans-bold.ttf', 40)
        img_drw.text(anchor, message, fill='orange', font=img_fnt)
        img_src.show()
        img_src.save(self.full_name)

    def mark_person(self): 
        if not self.response:
            raise("Found no annotation. Quit.")
        
        bb = self._extract_bb()
        if not bb:
            return None

        return self.snap_mark(bb)

class PresenceAI:
    def __init__(self):
        self.key = config.gcpkey

    def _convert_image_to_base64(self, snap):
        with open(snap.full_name, 'rb') as img:
            encoded_string = base64.b64encode(img.read()).decode()

        return encoded_string 

    def call_vision_api(self, snap):
        post_url = "https://vision.googleapis.com/v1/images:annotate?key=" + self.key

        base64_image = self._convert_image_to_base64(snap)

        post_payload = {
        "requests": [
            {
            "image": {
                "content" : base64_image
            },
            "features": [
                {
                "type": "OBJECT_LOCALIZATION",
                "maxResults": 10
                },
            ]
            }
        ]
        }

        result = requests.post(post_url, json=post_payload)
        result.raise_for_status()

        snap.request = post_payload
        snap.response = json.loads(result.text)

        return json.loads(result.text)
