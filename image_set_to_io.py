from pathlib import Path
import sys
import json
import os
import shutil

class JsonSerializer(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

jsonObjOut = []

PATH_TO_FILES = Path("/home/bernhard/Downloads/flickr30k_images/flickr30k_images").resolve()
STRUCTURE_OUTPUT = Path("./io_flickr").resolve()

if not STRUCTURE_OUTPUT.exists():
    os.mkdir(STRUCTURE_OUTPUT)
if not STRUCTURE_OUTPUT.joinpath("input").exists():
    os.mkdir(STRUCTURE_OUTPUT.joinpath("input"))
if not STRUCTURE_OUTPUT.joinpath("output").exists():
    os.mkdir(STRUCTURE_OUTPUT.joinpath("output"))

files = Path(PATH_TO_FILES).glob("*.jpg")

i = 0

for f in files:
    destIn = STRUCTURE_OUTPUT.joinpath("input").joinpath(f.name)
    destOut = STRUCTURE_OUTPUT.joinpath("output").joinpath(f.name)
    print(str(i) + ": " + str(f.name))

    dictObj = {
        "inputFileName": f.name,
        "outputFileName": f.name
    }
    jsonObjOut.append(dictObj)
    if not Path(destIn).exists():
        shutil.copyfile(f, destIn)
    if not Path(destOut).exists():
        shutil.copyfile(f, destOut)
    i = i + 1

handle = open(STRUCTURE_OUTPUT.joinpath("output").joinpath("original.id.id.json"), "w")
handle.seek(0)
handle.write(JsonSerializer().encode(jsonObjOut))
handle.close()
