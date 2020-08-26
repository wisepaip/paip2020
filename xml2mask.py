import numpy as np
import xml.etree.ElementTree as et
import os, glob, re
from tqdm import tqdm
import tifffile, cv2
import openslide

wsi_load_dir = './wsi_folder/'
xml_load_dir = './xml_folder/'
wsi_fns = sorted(glob.glob(wsi_load_dir + '*.svs') + glob.glob(wsi_load_dir + '*.SVS'))
xml_fns = sorted(glob.glob(xml_load_dir + '*.xml') + glob.glob(xml_load_dir + '*.XML'))
level = 2
div = 4**level                             ## Level0 scale to Level2 scale
assert len(wsi_fns) == len(xml_fns) == 47  ## the number of training_data WSI pool

save_dir = f'./mask_img_l{level}/'
os.makedirs(save_dir, exist_ok=True)

q = re.compile('training_data_[0-9]{2}')

'''
Annotations (root)
> Annotation (get 'Id' -> 1: tumor area)
 > Regions
  > Region (get 'NegativeROA' -> 0: positive area // 1: inner negative area)
   > Vertices
    > Vertex (get 'X', 'Y')
'''

def xml2mask(xml_fn, shape):
  # print('reconstructing sparse xml to contours of div={}..'.format(div))
  ret = dict()
  board_pos = None
  board_neg = None
  # Annotations >> 
  e = et.parse(xml_fn).getroot()
  e = e.findall('Annotation')
  assert(len(e) == 1), len(e)
  for ann in e:
    board_pos = np.zeros(shape[:2], dtype=np.uint8)
    board_neg = np.zeros(shape[:2], dtype=np.uint8)
    id_num = int(ann.get('Id'))
    assert(id_num == 1)# or id_num == 2)
    regions = ann.findall('Regions')
    assert(len(regions) == 1)
    rs = regions[0].findall('Region')
    plistlist = list()
    nlistlist = list()
    #print('rs:', len(rs))
    for i, r in enumerate(rs):
      ylist = list()
      xlist = list()
      plist, nlist = list(), list()
      negative_flag = int(r.get('NegativeROA'))
      assert negative_flag == 0 or negative_flag == 1
      negative_flag = bool(negative_flag)
      vs = r.findall('Vertices')[0]
      vs = vs.findall('Vertex')
      vs.append(vs[0]) # last dot should be linked to the first dot
      for v in vs:
        y, x = int(v.get('Y').split('.')[0]), int(v.get('X').split('.')[0])
        if div is not None:
          y //= div
          x //= div
        if y >= shape[0]:
          y = shape[0]-1
        elif y < 0:
          y = 0
        if x >= shape[1]:
          x = shape[1]-1
        elif x < 0:
          x = 0
        ylist.append(y)
        xlist.append(x)
        if negative_flag:
          nlist.append((x, y))
        else:
          plist.append((x, y))
      if plist:
        plistlist.append(plist)
      else:
        nlistlist.append(nlist)
    for plist in plistlist:
      board_pos = cv2.drawContours(board_pos, [np.array(plist, dtype=np.int32)], -1, [255, 0, 0], -1)
    for nlist in nlistlist:
      board_neg = cv2.drawContours(board_neg, [np.array(nlist, dtype=np.int32)], -1, [255, 0, 0], -1)
    ret[id_num] = (board_pos>0) * (board_neg==0)
  return ret

def save_mask(xml_fn, shape):
  wsi_id = q.findall(xml_fn)[0]
  save_fn = save_dir + f'{wsi_id}_l{level}_annotation_tumor.tif'
  ret = xml2mask(xml_fn, shape)
  tifffile.imsave(save_fn, (ret[1]>0).astype(np.uint8)*255, compress=9)

def load_svs_shape(fn, level=2):
  imgh = openslide.OpenSlide(fn)
  return [imgh.level_dimensions[level][1], imgh.level_dimensions[level][0]]


if __name__ == '__main__':
  for wsi_fn, xml_fn in tqdm(zip(wsi_fns, xml_fns), total=len(wsi_fns)):
    wsi_id = q.findall(wsi_fn)[0]
    xml_id = q.findall(xml_fn)[0]
    assert wsi_id == xml_id
    shape = load_svs_shape(wsi_fn, level=level)
    save_mask(xml_fn, shape)

