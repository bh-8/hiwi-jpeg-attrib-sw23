from pathlib import Path
import sys
import json

inputDirectory = Path("./io").resolve()

evaluationDictionary = {}

def evaluate(attribObj, attribType, attribName, stegoToolIdentifier):
    global evaluationDictionary

    stegoToolName = stegoToolIdentifier.split(".")[0]

    if not stegoToolIdentifier in evaluationDictionary:
        evaluationDictionary[stegoToolIdentifier] = {}
        evaluationDictionary[stegoToolIdentifier]["stegoTool"] = stegoToolName
    if not attribType in evaluationDictionary[stegoToolIdentifier]:
        evaluationDictionary[stegoToolIdentifier][attribType] = {}
    if not attribName in evaluationDictionary[stegoToolIdentifier][attribType]:
        evaluationDictionary[stegoToolIdentifier][attribType][attribName] = {}
    if not "_total" in evaluationDictionary[stegoToolIdentifier][attribType][attribName]:
        evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_total"] = 0
    evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_total"] += 1
    if not "_correct" in evaluationDictionary[stegoToolIdentifier][attribType][attribName]:
        evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_correct"] = 0
    if not "_correctRate" in evaluationDictionary[stegoToolIdentifier][attribType][attribName]:
        evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_correctRate"] = 0
    if not "_incorrect" in evaluationDictionary[stegoToolIdentifier][attribType][attribName]:
        evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_incorrect"] = 0
    if not "_incorrectRate" in evaluationDictionary[stegoToolIdentifier][attribType][attribName]:
        evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_incorrectRate"] = 0

    attribResult = attribObj[attribType][attribName]["result"]
    for attribTool in attribResult:
        if not attribTool in evaluationDictionary[stegoToolIdentifier][attribType][attribName] :
            evaluationDictionary[stegoToolIdentifier][attribType][attribName][attribTool] = 0
        evaluationDictionary[stegoToolIdentifier][attribType][attribName][attribTool] += 1
        if stegoToolName == attribTool:
            evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_correct"] += 1
            evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_correctRate"] = evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_correct"] / evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_total"]
        else:
            evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_incorrect"] += 1
            evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_incorrectRate"] = evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_incorrect"] / (evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_total"])

if not inputDirectory.exists():
    print("Could not find io directory at '" + str(inputDirectory) + "'!")
    sys.exit(10)

for jsonAttributionFile in list(inputDirectory.glob("*.attribution.json")):
    print("Evaluating '" + str(jsonAttributionFile) + "'...")
    jsonAttributionHandler = open(jsonAttributionFile)
    jsonAttribution = json.load(jsonAttributionHandler)

    stegoManipulation = jsonAttributionFile.name.split(".")[0] + "." + jsonAttributionFile.name.split(".")[1] + "." + jsonAttributionFile.name.split(".")[2]

    for attribution in jsonAttribution:
        for attrib in attribution["blindAttribs"]:
            evaluate(attribution, "blindAttribs", str(attrib), stegoManipulation)
        for attrib in attribution["nonBlindAttribs"]:
            evaluate(attribution, "nonBlindAttribs", str(attrib), stegoManipulation)

print("Writing results...")
handle = open(inputDirectory.joinpath("_attrib_evaluation.json"), "w")
handle.seek(0)
handle.write(json.dumps(evaluationDictionary))
handle.close()
print("Done!")
