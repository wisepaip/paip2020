# PAIP2020

Welcome to this PAIP2020 Forum.

Our main task is MSI-High classification in colorectal cancer.

If you have any question or comment, please post a message here.

## `xml2mask.py` utility code released

This is a code example for preprocessing the tumor area annotations which are given in \*.xml format.
Please set the proper parent directories to generate \*.tif pixel masks from \*.xml files.

- You need `openslide` package for loading metadata from \*.svs files.
  - https://openslide.org/download/
- The default conversion mode is set to make pixel masks in _Level2_ dimensions.
  - This downscale factor is highly likely to be the one for the user submissions.
    - It is tentative, so please check _Submit_ & _Evaluation_ tabs of [our challenge website](https://paip2020.grand-challenge.org/) afterward
    - To change this option, please do the followings:
      - change `div` number accordingly (default: 16, which means dimensions are divided by a factor of 16)
      - change rules for the directory and the filenames as you would like them to be
- FYI, dimensions of the given \*.svs files are downscaled by a factor of 4 per level.
  - e.g.
        
  | Level | (x \* y) |
  |:-----:|:--------:|
  | 0     | (100,000 \* 100,000) |
  | 1     | (25,000 \* 25,000) |
  | 2     | (6,250 \* 6,250) |
  | 3     | (1,562 \* 1,562) |
- Please leave questions if you have some issues using this code example.
