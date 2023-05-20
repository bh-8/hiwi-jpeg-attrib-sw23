# Jpeg attribution
More efficient implementation in Python featuring more detailed evaluation of identified jpeg stego attributes.
| attribution type | attribute | attribution tool | targeted stego tools |
| --- | --- | --- | --- |
| blind | JFIF version | exiftool | jsteg |
| blind | binwalk-extraction | binwalk | jsteg |
| blind | file header | strings | jsteg, f5, jphide, outguess, steghide |
| blind | foremost-extraction | foremost | jsteg |
| non-blind | file size | exiftool | jphide, steghide |
| non-blind | color mean | imagemagick, stegoveritas | jphide, steghide |
