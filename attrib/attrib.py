from jsonLog import LogEntry
from subprocess import run
import re

class Attribution():
    def __init__(self, jsonLog, sample, mime):
        self.jsonLog = jsonLog
        self.sample = sample
        self.mime = mime

        self.exiftoolData = None
        
    def blind(self):
        self.exiftoolData = open("./exiftool.tmp", "w")
        self.exiftoolData.seek(0)
        run([
            "exiftool",
            str(self.sample)
        ], stdout=self.exiftoolData)
        self.exiftoolData.close()

    def nonBlind(self, original):
        pass

    def flush(self):
        #TODO continue here.... but only with more diverse test samples
        #determine if JFIF version can be extracted by exiftool or not
        with open("./exiftool.tmp", "r") as tmpData:
            searchPattern = "JFIF Version"
            for l in tmpData:
                minL = l.strip().replace(" ", "")
                if re.search(searchPattern, l):
                    pass #print(minL)

        self.jsonLog.add(LogEntry(self.sample, self.mime))
