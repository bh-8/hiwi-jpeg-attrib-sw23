# JPEG attribution
INFO: This repository is discontinued. The attributes which found to perform the best (attributing `jsteg`, `f5` and `outguess`) have been implemented in a new JPEG analysis tool called [JPEG investigator](https://github.com/birnbaum01/hiwi-jpeg-investigator).
---
More efficient implementation in Python featuring more detailed evaluation of identified jpeg stego attributes.
| attribution type | attribute | attribution tool | targeted stego tools |
| --- | --- | --- | --- |
| blind | JFIF version | exiftool | jsteg |
| blind | binwalk-extraction | binwalk | jsteg |
| blind | file header | strings | jsteg, f5, jphide, outguess, steghide |
| blind | foremost-extraction | foremost | jsteg |
| non-blind | file size | exiftool | jphide, steghide |
| non-blind | color mean | imagemagick, stegoveritas | jphide, steghide |
