import sys
from pathlib import Path
from attrib import Attribution
import customProgress
import jsonLog

#lib-magic
import magic
mime = magic.Magic(mime=True)

INPUT_SAMPLES = Path("./samples").resolve()
TARGET_MIME = "image/jpeg"

# # # # # # # # # # # # # # # # # # # #

totalSampleCount = 0
for inputSample in list(INPUT_SAMPLES.glob("*")):
    if inputSample.is_file():
        inputMime = str(mime.from_file(inputSample))
        
        if TARGET_MIME == inputMime:
            totalSampleCount += 1

# # # # # # # # # # # # # # # # # # # #

progressBar = customProgress.ProgressBar("Attribution in progress...", max = totalSampleCount)
jsonLog = jsonLog.Log(Path("./samples/_attrib.json").resolve())

for inputSample in list(INPUT_SAMPLES.glob("*")):
    if inputSample.is_file():
        inputMime = str(mime.from_file(inputSample))
        
        if TARGET_MIME == inputMime:
            attr = Attribution(jsonLog, inputSample, inputMime)
            attr.blind()
            attr.nonBlind(None) #TODO: pass original here
            attr.flush()
            progressBar.next()

jsonLog.writeJson()
progressBar.finish()

sys.exit(0)
