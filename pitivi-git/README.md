# Pitivi Snap

This project is working toward a snap of Pitivi.

To get this done, we need to do the following:
 - add launcher
 - successfully build from current git

## Current state

At present, the build does not work with the `desktop/gtk3` part

Blocking error message:

```
Skipping build desktop/gtk3 (already ran)
'pitivi-edge' has prerequisites that need to be staged: desktop/gtk3
Skipping pull desktop/gtk3 (already ran)
Skipping build desktop/gtk3 (already ran)
Parts 'desktop/gtk3' and 'pitivi-edge' have the following file paths in common which have different contents:
usr/share/pkgconfig/shared-mime-info.pc
usr/share/pkgconfig/xkeyboard-config.pc
```

 
