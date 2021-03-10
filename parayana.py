from PIL import Image, ImageFont, ImageDraw
import os
import glob
import numpy as np
import scipy.stats as scs

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