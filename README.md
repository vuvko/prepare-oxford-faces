Scripts to prepare OXFORD VGG Face dataset
====================

Things I used to download and prepare dataset for experiments:
 * [aria2](https://aria2.github.io/) download utility. You can find all download links prepared in `vgg-faces-aria.txt`. To download simply type `aria2c -i vgg-faces-aria.txt --deferred-input -j 60`. It took approximatly 1.5 days and 100GB of space.
 * Python 2.7.11 with `pillow` module for image processing. You can crop all downloaded images with `python2 prepare.py` command.

Check dataset's [page](http://www.robots.ox.ac.uk/~vgg/data/vgg_face/) for more information.
