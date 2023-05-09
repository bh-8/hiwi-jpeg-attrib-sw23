from jsonLog import LogEntry
from subprocess import run
import re
from pathlib import Path
import shutil
import os
import glob

class Attribution():
    def __init__(self, jsonLog, sampleFile, originalFile, mime):
        self.jsonLog = jsonLog
        self.sampleFile = sampleFile
        self.originalFile = originalFile
        self.mime = mime
    
    def runAttribTool(self, toolId, execParams):
        outData = open("./" + toolId + ".tmp", "w")
        outData.seek(0)
        #print(str(execParams))
        run(execParams, stdout=outData, stderr=outData)
        outData.close()
        
    def blind(self):
        if Path("./foremost").exists():
            shutil.rmtree("./foremost")
        if Path("./compare_out.jpg").exists():
            os.remove("./compare_out.jpg")

        self.runAttribTool("exiftool", [
            "exiftool",
            str(self.sampleFile)
        ])
        self.runAttribTool("binwalk", [
            "binwalk",
            str(self.sampleFile)
        ])
        self.runAttribTool("strings", [
            "strings",
            str(self.sampleFile)
        ])
        self.runAttribTool("foremost", [
            "foremost",
            "-o", "./foremost",
            "-i", str(self.sampleFile)
        ])

    def nonBlind(self):
        #run exiftool on original image to compare file size
        self.runAttribTool("exiftool_orig", [
            "exiftool",
            str(self.originalFile)
        ])
        #diff. image
        self.runAttribTool("compare", [
            "compare",
            str(self.sampleFile),
            str(self.originalFile),
            "-compose", "src",
            "-highlight-color", "black",
            "./compare_out.jpg"
        ])
        self.runAttribTool("identify", [
            "identify",
            "-verbose",
            "./compare_out.jpg"
        ])
        self.runAttribTool("stegoveritas", [
            "stegoveritas",
            "-out",
            "./stegoveritas",
            "-meta",
            "-imageTransform",
            "-trailing",
            "-steghide",
            str(self.sampleFile)
        ])


    def flush(self):
        #https://github.com/birnbaum01/amsl-it-security-projects/blob/main/SMKITS5/stego-attrib.sh
        #TODO: missing exiftool file size comparison
        #TODO: missing stegoveritas diff. image creation+analysis
        #TODO: missing attrib evaluation as 3rd field in log file: conclusion

        ATTR_JFIF_VERSION = None
        with open("./exiftool.tmp", "r") as tmpData:
            searchPattern = "JFIF Version:"
            for l in tmpData:
                minL = l.strip().replace("  ", "")
                if re.search(searchPattern, minL):
                    ATTR_JFIF_VERSION = minL
                    break
        
        ATTR_BINWALK = None
        with open("./binwalk.tmp", "r") as tmpData:
            tmpLines = tmpData.readlines()
            if len(tmpLines) > 4:
                ATTR_BINWALK = tmpLines[3].strip().replace("  ", "")

        ATTR_FILE_HEADER = None
        with open("./strings.tmp", "r") as tmpData:
            tmpLines = tmpData.readlines()
            if len(tmpLines) > 0:
                ATTR_FILE_HEADER = ""
                for i in range(0, 10):
                    if len(tmpLines) > i:
                        ATTR_FILE_HEADER += tmpLines[i]

        ATTR_FOREMOST = None
        if Path("./foremost/jpg/00000000.jpg").exists():
            ATTR_FOREMOST = "carved, extracted jpg"
            
        ATTR_COLOR_MEAN_DIFF = None
        with open("./identify.tmp", "r") as tmpData:
            searchPattern = "mean:"
            for l in tmpData:
                minL = l.strip().replace("  ", "")
                if re.search(searchPattern, minL):
                    ATTR_COLOR_MEAN_DIFF = minL
                    break

        self.jsonLog.add(LogEntry(
            str(self.sampleFile.name),
            str(self.originalFile.name),
            str(self.mime),
            ATTR_JFIF_VERSION,
            ATTR_BINWALK,
            ATTR_FILE_HEADER,
            ATTR_FOREMOST,
            ATTR_COLOR_MEAN_DIFF
        ))
