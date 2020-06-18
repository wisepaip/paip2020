# PAIP2020

Welcome to this PAIP2020 Forum.

Our main task is MSI-High classification in colorectal cancer.

If you have any question or comment, please post a message here.


**Recent inquiry
1. Non-masked regions (= normal tissue) contain no MSI : Masked regions could include the MSI or not, however, non-masked regions are all normal tissues. Thus, no MSI information are in the non-masked regions.
2. Blank area  in the masked regions (= empty space = background) : Based on weak supervision, our task has been set to be more challenging than last year. Thus, the blank area has not been removed, participants have to deal with it if necessary. (you can refer the criteria of blank area in last challenge PAIP2019. https://paip2019.grand-challenge.org/Dataset/)

3. All WSIs were scanned at 40X magnification and all cases are randomly selected irrespective of the participating institutions.

4. Recently in regard to the submission of data use agreement, the file upload form provided by Google does not work properly.
Our engineering team have checked and also contacted Google to report about this, but have not yet received a clear answer.
Thus, if any participant are experiencing this problem, please send the data use agreement file (pdf format) that you have written to the organizer directly by e-mail. mailto : paip.challenge@gmail.com
We apologize for any inconvenience.

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
