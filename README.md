![](logo.png)

File organizer for [PS-IO](https://ps-io.com/). To be an organizing tool it's really messy because I'm constantly playing with it as a proof of concept. It's just quicker for me to write an ugly Python tool than to organize my files by hand. Also it can be reused for when I want to generate hashes for the NTSC-J set and or whenever I find the latest redump.

Which reminds me: if you have the latest redump set you can A) send a link my way and/or 2) generate a hashes file by using the `datscript.py` script on the corresponding `Datfile.dat` available on the [Redump website](http://redump.org/downloads/).

I've generated the supplied `hashes.json` by running the `cuehasher.py` script on my own set. This is _probably_ a really shitty way to do this but I needed it to work _once_ and it only takes a manageable amount of manual labor to tweak the data set until it works. From then on it's smooth sailing.

Let's talk about what this is.

## What this is
Okay. **psiorganizer** is super domain specific and it satisfies my needs. However, if you have the same needs you might benefit from using **psiorganizer** as well.

If you have a PS-IO and the most common Redump set (**20150524**) (currently only the NTSC-U region) and you want an automatic way to import games from this set to a PS-IO friendly and you friendly structure then _we are in the same boat_.

If you have Mednafen and a fresh RAR archive from an ad revenue financed rom site forum then we do not have the same needs and you should close this tab. 

## Features

* Imports your games to a formatted directory structure
* Merges tracks into single binary blob using [binmerge](https://github.com/putnam/binmerge)
* Generates CU2 files using [cue2cu2](https://github.com/NRGDEAD/Cue2cu2)
* Generates mutlidisk files

## Future Features Maybe


* Adds cover images to imported games
* Downloads and imports the latest firmware

## Usage

With the proper Python 3 in your shell:

```sh
$ psiorganizer -i ~/roms/playstation/ntsc-u -o /dev/sdb1 -d ../lib/discs.json -m ../lib/hashes.json
```

Input `-i` is where your games are.  
  
Output `-o` is where your SD card is. 
  
Discs `-d` is where `discs.json` is (probably in `/lib/`).
  
Hashes `-m` is where the `hashes.json` is (again, probably in `/lib/`).

This turn this mess:

```
~/Downloads
  Top 10 PSX Games + ePSXe & ESSENTIAL PLUGINS (2.1)/
    roms/
      Game_title/
        game.title.disc1.cue
        game.title.disc1.track1.bin
        game.title.disc1.track2.bin
        game.title.disc1.track3.bin
        game.title.disc1.track4.bin
        game.title.disc1.track5.bin
        game.title.disc1.track6.bin
        game.title.disc1.track7.bin
        game.title.disc1.track8.bin
        game.title.disc2.track1.bin
        game.title.disc2.track2.bin
        game.title.disc2.track3.bin
        game.title.nfo
        Download-More-On-Demonoid!.txt
```

Into this glorious order:

```
/ 
  Game Title/ 
    Game Title (Disc 1).bin
    Game Title (Disc 1).cue
    Game Title (Disc 1).cu2
    Game Title (Disc 2).bin
    Game Title (Disc 2).cue
    Game Title (Disc 2).cu2
    MULTIDISC.LST
```

## Contribute

Not importing your game? Missing feature? Ugly python? Contribute.

## License
BSD 2 baby

## Third party legal
I'm not sure how to do this but let's do legal disclaimers starting with Cue2cue:

Do you have an abundance of cuesheets and a sore lack of CU2-files? Look no further, Cue2cue by my good equal NRGDEAD.

It has a lot of features and a LICENSE that we might inspect right here:

```
Copyright 2019-2020 NRGDEAD

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
```

Now, for all you individual track-having unmerged lurkers. The cure for your chronic ailment is here. BINMERGE. Concatenate all binaries. The license is super long so [link](https://github.com/putnam/binmerge/blob/master/LICENSE)