from jsonLog import LogEntry
from subprocess import run
import re
from pathlib import Path
import shutil
import os
import glob

class Attribution():
    def __init__(self, jsonLog, sampleFile, originalFile, mime, blindAttribOnly = False):
        self.jsonLog = jsonLog
        self.sampleFile = sampleFile
        self.originalFile = originalFile
        self.mime = mime
        self.blindAttribOnly = blindAttribOnly
    
    def runAttribTool(self, toolId, execParams):
        outData = open("./" + toolId + ".tmp", "w")
        outData.seek(0)
        #print(str(execParams))
        run(execParams, stdout=outData, stderr=outData)
        outData.close()
    
    def execute(self):
        if Path("./foremost").exists():
            shutil.rmtree("./foremost")
        if Path("./stegoveritas_stego").exists():
            shutil.rmtree("./stegoveritas_stego")
        if Path("./stegoveritas_original").exists():
            shutil.rmtree("./stegoveritas_original")

        if Path("./compare_out.jpg").exists():
            os.remove("./compare_out.jpg")
        if Path("./compare_red.png").exists():
            os.remove("./compare_red.png")
        if Path("./compare_green.png").exists():
            os.remove("./compare_green.png")
        if Path("./compare_blue.png").exists():
            os.remove("./compare_blue.png")

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

        if not self.blindAttribOnly:
            self.runAttribTool("exiftool_orig", [
                "exiftool",
                str(self.originalFile)
            ])
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
                "./stegoveritas_original",
                "-imageTransform",
                str(self.originalFile)
            ])
            self.runAttribTool("stegoveritas", [
                "stegoveritas",
                "-out",
                "./stegoveritas_stego",
                "-meta",
                "-imageTransform",
                "-trailing",
                "-steghide",
                str(self.sampleFile)
            ])
            self.runAttribTool("compare_red", [
                "compare",
                "./stegoveritas_stego/" + self.sampleFile.name + "_red_plane.png",
                "./stegoveritas_original/" + self.originalFile.name + "_red_plane.png",
                "-compose", "src",
                "-highlight-color", "black",
                "./compare_red.png"
            ])
            self.runAttribTool("compare_green", [
                "compare",
                "./stegoveritas_stego/" + self.sampleFile.name + "_green_plane.png",
                "./stegoveritas_original/" + self.originalFile.name + "_green_plane.png",
                "-compose", "src",
                "-highlight-color", "black",
                "./compare_green.png"
            ])
            self.runAttribTool("compare_blue", [
                "compare",
                "./stegoveritas_stego/" + self.sampleFile.name + "_blue_plane.png",
                "./stegoveritas_original/" + self.originalFile.name + "_blue_plane.png",
                "-compose", "src",
                "-highlight-color", "black",
                "./compare_blue.png"
            ])
            self.runAttribTool("identify_red", [
                "identify",
                "-verbose",
                "./compare_red.png"
            ])
            self.runAttribTool("identify_green", [
                "identify",
                "-verbose",
                "./compare_green.png"
            ])
            self.runAttribTool("identify_blue", [
                "identify",
                "-verbose",
                "./compare_blue.png"
            ])

    def convertFileSize(self, fileSizeStr):
        split = fileSizeStr.split(":")[1].strip().split(" ")
        num = float(split[0])
        unit = split[1].lower()
        match unit:
            case "bytes":
                return num
            case "kib":
                return num * 1024
            case "mib":
                return num * 1024 * 1024
            case _:
                return -1

    def parseFileSize(self, exiftoolId):
        with open("./" + exiftoolId + ".tmp", "r") as tmpData:
            searchPattern = "File Size"
            for l in tmpData:
                minL = l.strip().replace("  ", "")
                if re.search(searchPattern, minL):
                    return int(self.convertFileSize(minL))
        return -1

    def parseColorMean(self, identifyId):
        with open("./" + identifyId + ".tmp", "r") as tmpData:
            searchPattern = "mean:"
            for l in tmpData:
                minL = l.strip().replace("  ", "")
                if re.search(searchPattern, minL):
                    return minL
            return None

    def attribute(self):
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

        ATTR_FILE_SIZE = None
        ATTR_COLOR_MEAN_DIFF_DRGB = None

        if not self.blindAttribOnly:
            stegoFileSize = self.parseFileSize("exiftool")
            originalFileSize = self.parseFileSize("exiftool_orig")
            ATTR_FILE_SIZE = "Stego File: " + str(stegoFileSize) + ", Original File: " + str(originalFileSize) + ", Difference: " + str(abs(stegoFileSize - originalFileSize))

            colorMeanDiffRed = self.parseColorMean("identify_red")
            colorMeanDiffGreen = self.parseColorMean("identify_green")
            colorMeanDiffBlue = self.parseColorMean("identify_blue")
            ATTR_COLOR_MEAN_DIFF_DRGB = str(self.parseColorMean("identify")) + ", " + str(colorMeanDiffRed) + ", " + str(colorMeanDiffGreen) + ", " + str(colorMeanDiffBlue)

        self.jsonLog.add(LogEntry(
            str(self.sampleFile.name),
            str(self.originalFile.name),
            str(self.mime),
            ATTR_JFIF_VERSION,
            ATTR_BINWALK,
            ATTR_FILE_HEADER,
            ATTR_FOREMOST,
            ATTR_FILE_SIZE,
            ATTR_COLOR_MEAN_DIFF_DRGB
        ))
