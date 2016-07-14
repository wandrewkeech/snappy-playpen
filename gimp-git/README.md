# GIMP-from-git snap

This project is a work in progress to build GIMP (and its dependencies)
from the git repositories.

## Current State

The old blocking bug with `pkg-config` not properly picking up on earlier
parts of the snap during the `stage` phase has been resolved. The `gimp`
application itself almost completely builds, and though I don't have time
at the moment of writing this update, I feel like the present bug could be
resolved with defining some env vars explicitly.
