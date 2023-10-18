# JPEG attribution
### FEATURES MOVED, REPOSITORY DISCONTINUED
The attributes which found to perform the best (attributing `jsteg`, `f5` and `outguess`) have been implemented in a new JPEG analysis tool called [JPEG investigator](https://github.com/birnbaum01/hiwi-jpeg-investigator).
This repository will remain online only for transparency reasons; it was used to generate data in "*Stego-Malware Attribution: Simple Signature and Content-based Features Derived and Validated from Classical
Image Steganalysis on Five Exemplary Chosen Algorithms*" ([SECURWARE'23](https://www.thinkmind.org/index.php?view=instance&instance=SECURWARE+2023), p. 33-42)

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
