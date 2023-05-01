from json import JSONEncoder

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
    def __init__(self, sampleName, originalName, detectedMimeType, jfifVersion, binwalk, fileHeader, foremost, diffColor):
        self.sampleName = sampleName
        self.originalName = originalName
        self.detectedMimeType = detectedMimeType
        self.blindAttribs = {
            "jfifVersion": {
                "attribTool": "exiftool",
                "data": jfifVersion
            },
            "binwalkData": {
                "attribTool": "binwalk",
                "data": binwalk
            },
            "fileHeader": {
                "attribTool": "strings",
                "data": fileHeader
            },
            "foremostCarving": {
                "attribTool": "foremost",
                "data": foremost
            }
        }
        self.nonBlindAttribs = {
            "colorMeanDifference": {
                "attribTool": "imagemagick",
                "data": diffColor
            }
        }
