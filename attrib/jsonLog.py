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
    def __init__(self, sample, mime):
        self.sample = str(sample)
        self.mime = str(mime)
