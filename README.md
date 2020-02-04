# psiorganizer

File organizer for [PS-IO](https://ps-io.com/).

## Features

* None

## Planned Features

* Imports your games to a formatted directory structure.
* Adds a cover image to imported games.
* Automatically generates mutlidisk files.
* Downloads and imports the latest firmware.

## Usage

Input is where your games are and output is where your SD card is:

```sh
$ psiorganizer -i ~/roms/playstation/ntsc-u -o /dev/sdb1
```

This will import your games like so:

```
/
  USA/
    Game Title/
      COVER.BMP   
      Game Title (Disc 1).bin
      Game Title (Disc 1).cue
      Game Title (Disc 2).bin
      Game Title (Disc 2).cue
      MULTIDISC.LST
```

## Contribute

Not importing your game? Cover art missing? Contribute.