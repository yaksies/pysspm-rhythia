# pysspm-rhythia

The official python library dedicated to reading, writing, and modifying the SSPM file format from the video game "Rhythia".

> ***Note: Any version before 0.1.5 does not work in python.***

## SSPM libray information

The main library includes these features:

> 1. Reading .SSPM files
> 2. Modifying SSPM data
> 3. Writing .SSPM files

Extras:

> 1. Difficulty Calculation (W.I.P)
> 2. Note Classification (semi-stable)

## How to install/use

To install the library, run:

```bash
pip install pysspm-rythia
```

to start using the library, create a python script and load up pysspm.

```python
from pysspm_rhythia import SSPMParser


parser = SSPMParser()

# Example of loading a SSPMfile
parser.ReadSSPM("*.sspm")

# Example of turning it into a roblox sound space file

with open("output.txt", "w") as f:
    f.write(parser.NOTES2TEXT())

```

> *Functionality does not end there. When reading files, you have full access to all the metadata, and other information stored in the variables.*

**Some common variables you will find are:**

1. `coverBytes` the byteform of the image if cover was found
2. `audioBytes` the byteform of the audio in `.mp3` form if audio was found
3. `Header`: {"Signature": ..., "Version": ...}
4. `Hash`: a SHA-1 hash of the markers (notes) in the map
5. `mapID`: A unique combination using the mappers and map name*
6. `mappers`: a list containing each mapper.
7. `mapName`: The name given to the map.
8. `songName`: The original name of the audio before imported. Usually left as artist name - song name
9. `customValues`: NOT IMPLEMENTED | will return a dictionary of found custom blocks.
10. `isQuantum`: Determins if the level contains ANY float value notes.
11. `Notes`: A list of tuples containing all notes. | Example of what it Notes is: `[(x, y, ms), (x, y, ms), (x, y, ms) . . .]`

```python
from pysspm_rhythia import SSPMParser


parser = SSPMParser()

# Example of loading a SSPMfile
parser.ReadSSPM("*.sspm")

# changing the decal to be a different image
if parser.hasCover[0] == 0: # hasCover is originally in byteform | Can be 0x00 or 0x01
    with open("cover.png", 'rb') as f:
        parser.coverBytes = f.read() # reading the BYTES of the image

# Finally save the sspm file with the newly configured settings
sspmFileBytes = parser.WriteSSPM()

with open('sspmfile.sspm', "wb") as f:
    f.write(sspmFileBytes)

```

Alternativly, you can pass in arguments into WriteSSPM function directly

```py
from pysspm_rhythia import SSPMParser

parser = SSPMParser()
parser.ReadSSPM("*.sspm")

mappers = parser.Mappers.extend('DigitalDemon') # adding another mapper to the mapper list
parser.WriteSSPM('./SSPMFile.sspm', mappers=mappers)
```

## Advanced guide

This shows the more advanced things you can do by giving examples of custom written code.

```python
from pysspm_rhythia import SSPMParser
from random import randint

parser = SSPMParser()

parser.ReadSSPM("*.sspm") # reading the sspm file

sigHeader = parser.Header.get("Signature") # 4 byte header | should always be: b"\x53\x53\x2b\x6d"
ver = parser.Header.get("Version") # stored as 2 or 1
sspmHash = parser.Hash # Storing the hash

if randint(0, 5) == 5:
    parser.Notes = parser.Notes.extend((1, 1, (parser.Notes[-1][2]+200))) # adding a center note (1,1), with ms of last note + 200

newSSPM = parser.WriteSSPM(mappers=["DigitalDemon", "Someone else"], mapName="Possibly modified map haha")

# comparing the note hashes
newSSPMHash = parser.Hash
if newSSPMHash == sspmhash:
    with open("UnmodifiedMap.sspm", 'wb') as f:
        f.write(newSSPM)
else:
    raise Warning("Map does not match original hash. Map notes were modified from the original!!!")


```

> Code shows off how hashes are calculated to prevent changes between levels. Could be used for security and integrity of the notes.

*More advanced documentation will be added in the near future...*

## Function Documentation

A in-depth list of things you can do with this library

```py
SSPMParser()
```

> Initializes the sspm library parser

```py
def WriteSSPM(self, filename: str = None, debug: bool = False, **kwargs) -> bytearray | None:
```

> Creates a SSPM v2 file based on variables passed in, or already set.

*If no filepath is passed in, it will return file as bytes* <br>
*Note: current version of pysspm-rhythia requires audio as a parameter for v2 filetype*

**Variables that need to be covered:**

1. `coverImage`: Cover image in bytes form, or None
2. `audioBytes`: Audio in bytes form, or None
3. `Difficulty`: one of Difficulties dictionary options, or 0x00 - 05 OR "N/A", "Easy", "Medium", "Hard", "Logic", "Tasukete"
4. `mapName`: The name of the map. Rhythia guidelines suggests `artist name - song name`
5. `mappers`: a list of strings containing the mapper(s)
6. `notes`: a list of tuples as shown below

<br>

```python
# (x, y, ms)
self.notes = [
 (1, 2, 1685), # X, Y, MS
 (1.22521, 0.156781, 2000)
]#...
```

***Notes can sometimes be unordered***

<br>

`**kwargs`: pass in any of the variables shown above.

Example usage:

```python
    from pysspm_rhythia import SSPMParser
        
    sspm = SSPMParser()
    sspm.ReadSSPM("*.sspm") # reads
    sspm.Difficulty = 5 # changes difficulty to Tasukete
        
    with open(output_path+".sspm", "wb") as f:
        f.write(sspm.WriteSSPM())
```

**ReadSSPM**

```py
def ReadSSPM(self, file: str | BinaryIO, debug: bool = False):
```

> Reads and processes any SSPM file. <br>

`File:` Takes in directory of sspm, or BinaryIO object stored in memory.
`debug:` Useful for getting readable outputs of steps taken.

#### Warning

***SSPM (Sound space plus map file) version 1 is not supported at this time. loading this file may raise errors***

#### Returns

1. `coverBytes` if cover was found
2. `audioBytes` if audio was found
3. `Header`: {"Signature": ..., "Version": ...}
4. `Hash`: a SHA-1 hash of the markers in the map
5. `mapID`: A unique combination using the mappers and map name*
6. `mappers`: a list containing each mapper.
7. `mapName`: The name given to the map.
8. `songName`: The original name of the audio before imported. Usually left as artist name - song name
9. `customValues`: NOT IMPLEMENTED | will return a dictionary of found custom blocks.
10. `isQuantum`: Determins if the level contains ANY float value notes.
11. `Notes`: A list of tuples containing all notes.

Example of what it Notes is: `[(x, y, ms), (x, y, ms), (x, y, ms) . . .]`

> ***Returns itself***

## Roadmap (May get completed)

TODO: (In order of priority)

- Add typing support for library ✔️
- add proper documentation on github
- add proper documentation in code ✔️
- add loading of sspmV2  ✔️
- add support for creating sspmV2 ✔️
- clean up unused variables from @self ✔️
- add support for sspmv1 loading ✔️ (Thank you fogsaturate)
- support multiple versions of sspm
- add custom block support in loading
- Drop numpy dependency
- Implement Extras difficulty calc
- Implement simple note ordering function
- Support for Pheonix Filetype (When I get my hands on the data structure)

Made with 💖 by DigitalDemon (David Jed)

> Documentation last updated: `2024-12-12` | `V0.2.2`
