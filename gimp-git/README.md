# GIMP-from-git snap

This project is a work in progress to build GIMP (and its dependencies)
from the git repositories.

Configured to build with:
  - GEGL from git
  - libmypaint for MyPaint brushes
  - GMIC from the Ubuntu repositories

## Current State

Thanks for `dholbach` and the new Snappy Sandpit!

Sadly new `snapcraft` superpowers have not magically solved the problems
with the automated `autotools` build. Currently the build breaks during
`gegl`'s compilation (the specific target is `Gegl-0.3.gir`). Error output
as follows (slightly edited):

```
GISCAN   Gegl-0.3.gir
<command-line>:0:0: warning: "G_LOG_DOMAIN" redefined
<command-line>:0:0: note: this is the location of the previous definition
/usr/bin/ld: [...]/snappy-playpen/gimp-git/stage/lib/libbabl-0.1.a(babl-extension.o): undefined reference to symbol 'dlclose@@GLIBC_2.2.5'
//lib/x86_64-linux-gnu/libdl.so.2: error adding symbols: DSO missing from command line
collect2: error: ld returned 1 exit status
linking of temporary binary failed: Command '['/bin/bash', '../libtool', '--mode=link', '--tag=CC', '--silent', 'gcc', '-o', '.../snappy-playpen/gimp-git/parts/gegl/build/gegl/tmp-introspectCo_9dN/Gegl-0.3', '-export-dynamic', '-I.../snappy-playpen/gimp-git/stage/include', '-I.../snappy-playpen/gimp-git/stage/include][a whole bunch of flags]' returned non-zero exit status 1
/usr/share/gobject-introspection-1.0/Makefile.introspection:155: recipe for target 'Gegl-0.3.gir' failed
make[3]: *** [Gegl-0.3.gir] Error 1
```
