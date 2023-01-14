## v1.0

First release

## v1.1

New stuff:
- Added ReplayBot support

Changes:
- Put "All files" first as the default file extension when selecting a macro to avoid confusion

Bug fixes:
- Fixed allowing click generation if macro/clickpack/output path was an empty string
- Fixed parser errors taking input and then exiting
- Fixed reading binary macros as text

## v1.2

New things:
- **Clickpacks can now have hardclicks**
- Added ability to disable softclicks/hardclicks
- Added ability to disable random softclick/hardclick delay
- New macro info panel
- New custom theme

Changes:
- **Complete UI redesign**
- Optimized softclick/hardclick delay randomization
- Optimized parsing ReplayBot macros

Bug fixes:
- Fixed parsing the replay/clickpack/output selected even if nothing was selected
- Fixed output files not have a .wav extension

## v1.3

New stuff:
- Added plain text support
- Added a bunch of options for controlling output audio

Changes:
- Moved click generation to a seperate python file
- Changed how the script path was read to be compatible wtih pyinstaller

Bug fixes:
- Fixed ReplayBot macros inserting random releases at the end of the macro
- Fixed zcb-gui throwing an error if you closed the macro selection without selecting a macro

## v1.4

New stuff:
- **Added an update checker**
- **Added support for MHR Binary macros**
- **Clickpack audio files are no longer limited to wav files**

Changes:
- **Rewrote click discovery and click generation from scratch**
- Made UI more streamlined and compact
- Code formatted to meet [PEP 8](https://peps.python.org/pep-0008/) specifications

Bug fixes:
- Fixed ZBot macros calling the wrong function (how did i mess this up)
- Fixed not selecting a macro to throw an error (again)
- Fixed a lot of things which were broken on Linux
