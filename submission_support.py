'''
  The code snippet below includes:
  1) a compression method to apply on your final result masks and
  2) its simple usage example
'''

import tifffile
import numpy as np

def imsave_paip2020(filename, img):
  # assuming that the img is always a binarized mask
  # NOTE: Please match the scale of the mask to 'Level2' scale of the corresponding WSI.
  assert filename[-4:] == '.tif', 'File ext name must be \'.tif\''
  img = np.array(img, dtype=np.uint8)
  tifffile.imsave(filename, img, compress=9)

if __name__ == '__main__':
  # assuming that we already have something to save on memory, named 'something_to_save'
  # and assuming that we already have 'submission01/' directory
  imsave_paip2020('submission01/validation_data_01.tif', something_to_save)

