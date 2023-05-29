import sys
from pathlib import Path
from attrib import Attribution
import customProgress
import jsonLog
import json

#lib-magic
import magic
mime = magic.Magic(mime=True)

JPG_MIME = "image/jpeg" #jpg images only
STEGO_TOOLS = ["f5", "jphide", "jsteg", "outguess", "steghide", "imrecompjpg"] #tools we can attribute

INPUT_STRUCTURE = Path("./io").resolve()
PATH_ORIG = INPUT_STRUCTURE.joinpath("./input")
PATH_STEGO = INPUT_STRUCTURE.joinpath("./output")

# # # # # # # # # # # # # # # # # # # #

if not INPUT_STRUCTURE.exists():
    print("Error: Could not find io structure: '" + str(INPUT_STRUCTURE) + "'!")
    sys.exit(10)
if not PATH_ORIG.exists():
    print("Error: IO input does not exist: '" + str(PATH_ORIG) + "'!")
    sys.exit(11)
if not PATH_STEGO.exists():
    print("Error: IO output does not exist: '" + str(PATH_ORIG) + "'!")
    sys.exit(12)

# # # # # # # # # # # # # # # # # # # #

#loop target tool ids
for stegoToolId in STEGO_TOOLS:
    #loop json logs
    for stegoLogFile in list(PATH_STEGO.glob(stegoToolId + ".*.json")):
        jsonHandle = open(stegoLogFile)
        jsonData = json.load(jsonHandle)
        
        progressBar = customProgress.ProgressBar("Attributing '" + str(stegoLogFile.name) + "'...", max = len(jsonData))
        jsonLogObj = jsonLog.Log(INPUT_STRUCTURE.joinpath(Path(str(stegoLogFile)).stem + ".attribution.json"))

        for toolExecution in jsonData:
            ##########
            # QA

            potentialStegoFileName = toolExecution["outputFileName"]
            if potentialStegoFileName == None:
                progressBar.next()
                continue

            potentialStegoFile = PATH_STEGO.joinpath(potentialStegoFileName)
            if not potentialStegoFile.is_file():
                progressBar.next()
                continue

            relatedOriginalFileName = toolExecution["inputFileName"]
            relatedOriginalFile = PATH_ORIG.joinpath(relatedOriginalFileName)
            if not relatedOriginalFile.is_file():
                progressBar.next()
                continue

            #do not use mime type to check format, as image file format structure could be corrupted
            inputMime = str(mime.from_file(potentialStegoFile))
            #if inputMime != JPG_MIME:
            #    progressBar.next()
            #    continue
            if not potentialStegoFileName.lower().endswith((".jpg", ".jpeg")):
                progressBar.next()
                continue

            ##########
            # Attribution

            attr = Attribution(jsonLogObj, potentialStegoFile, relatedOriginalFile, inputMime)
            attr.execute()
            attr.attribute()

            progressBar.next()

        jsonHandle.close()
        jsonLogObj.writeJson()
        progressBar.finish()
sys.exit(0)
