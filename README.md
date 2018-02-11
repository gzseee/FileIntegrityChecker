# FileIntegrityChecker

Basic tool for automated file integrity checking using existing software. It can be useful after recovery from damaged media or archives.

Note that even though verification will pass, will be still be damaged.

No guarantees. Use at your own risk.

## Prerequisites

Tool currently has following dependencies:

  * videos: ffmpeg in path
    - mp4, avi, mov, mts, 3gp
  * images: PIL python module
    - jpg, thm, ppm, jpeg, tiff, bmp, eps, gif, im, msp, pcx, png
  * zip archives: zipfile python module
    - zip

## Usage

Scanning a folder is as simple as

```
./fic.py --files folder/
```
