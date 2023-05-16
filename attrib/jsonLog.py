from json import JSONEncoder
from evaluate import evaluate

class LogJsonEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class Log():
    def __init__(self, jsonFile):
        self.log = []
        self.jsonFile = jsonFile
    def add(self, entry):
        self.log.append(entry)
    def asJson(self):
        return LogJsonEncoder().encode(self.log)
    def writeJson(self):
        handle = open(self.jsonFile, "w")
        handle.seek(0)
        handle.write(self.asJson())
        handle.close()

class LogEntry():
    def __init__(self, sampleName, originalName, detectedMimeType, jfifVersion, binwalk, fileHeader, foremost, fileSize, diffColor, diffColorRgb):
        #TODO: missing attrib evaluation as 3rd field in log file: conclusion
        # #https://github.com/birnbaum01/amsl-it-security-projects/blob/main/SMKITS5/stego-attrib.sh
        self.sampleName = sampleName
        self.originalName = originalName
        self.detectedMimeType = detectedMimeType
        self.blindAttribs = {
            "jfifVersion": {
                "attribTool": "exiftool",
                "data": jfifVersion,
                "result": evaluate("jfifVersion", jfifVersion)
            },
            "binwalkData": {
                "attribTool": "binwalk",
                "data": binwalk,
                "result": evaluate("binwalkData", binwalk)
            },
            "fileHeader": {
                "attribTool": "strings",
                "data": fileHeader,
                "result": evaluate("fileHeader", fileHeader)
            },
            "foremostCarving": {
                "attribTool": "foremost",
                "data": foremost,
                "result": evaluate("foremostCarving", foremost)
            }
        }
        self.nonBlindAttribs = {
            "fileSize": {
                "attribTool": "exiftool",
                "data": fileSize,
                "result": evaluate("fileSize", fileSize)
            },
            "colorMeanDifference": {
                "attribTool": "imagemagick",
                "data": diffColor,
                "result": evaluate("colorMeanDifference", diffColor)
            },
            "colorMeanDifferenceRgb": {
                "attribTool": "stegoveritas, imagemagick",
                "data": diffColorRgb,
                "result": evaluate("colorMeanDifferenceRgb", diffColorRgb)
            }
        }
