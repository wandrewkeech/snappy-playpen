# GIMP-from-git snap

This project is a work in progress to build GIMP (and its dependencies)
from the git repositories.

Configured to build with:
  - GEGL from git
  - libmypaint for MyPaint brushes
  - GMIC from the Ubuntu repositories

## Current State

Thanks for `dholbach` and the new Snappy Sandpit!

Changed the approach to `snapcraft`ing from source, from static binaries
to dynamic binaries, using the `install-via: prefix` property for the
`autotools` plug-in. Build seems to be going much better, but running into
an issue I've had before. A module in GEGL for n-point deformation
segfaults very consistently on Ubuntu (in my experience). I don't know why
it work sometimes and not others. Error output as follows:

```
Generating example images ../tools/gobj2dot.rb .. | /usr/bin/dot -Tpng
[... a couple tests...]
gegl:npd
/bin/bash: line 6: 178855 Segmentation fault      (core dumped)
GEGL_SWAP=RAM GEGL_PATH=../operations ../tools/gegl-tester --all -o
images/examples -d ./images -e
"load|buffer-source|pixbuf|nop|clone|convert-format|introspect|layer|image-compare|load|open-buffer|svg-load|exr-load|jpg-load|png-load|magick-load|box-blur|stretch-contrast|remap|matting-global|exp-combine|dropshadow|kuwahara|box-percentile|disc-percentile|snn-percentile|line-profile|buffer-cache|warp|mandelbrot|hstack"
Makefile:778: recipe for target 'examples' failed
```
