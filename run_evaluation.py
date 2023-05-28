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

    if not "_correct_in_list" in evaluationDictionary[stegoToolIdentifier][attribType][attribName]:
        evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_correct_in_list"] = 0
    if not "_incorrect_in_list" in evaluationDictionary[stegoToolIdentifier][attribType][attribName]:
        evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_incorrect_in_list"] = 0
    if not "_true_positives" in evaluationDictionary[stegoToolIdentifier][attribType][attribName]:
        evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_true_positives"] = 0
    if not "_false_positives" in evaluationDictionary[stegoToolIdentifier][attribType][attribName]:
        evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_false_positives"] = 0
    if not "_true_negatives" in evaluationDictionary[stegoToolIdentifier][attribType][attribName]:
        evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_true_negatives"] = 0
    if not "_false_negatives" in evaluationDictionary[stegoToolIdentifier][attribType][attribName]:
        evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_false_negatives"] = 0

    attribResult = attribObj[attribType][attribName]["result"]

    if(len(attribResult) == 0): #if no tools in result list --> attributed as original image
        if stegoToolName == "imrecompjpg": #if true negative TODO: OR -> add flickr later
            evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_true_negatives"] += 1
        else:
            evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_false_negatives"] += 1
    else:
        for attribTool in attribResult:
            #count apparent tool detects
            if not attribTool in evaluationDictionary[stegoToolIdentifier][attribType][attribName]:
                evaluationDictionary[stegoToolIdentifier][attribType][attribName][attribTool] = 0
            evaluationDictionary[stegoToolIdentifier][attribType][attribName][attribTool] += 1

            if stegoToolName == attribTool:
                if(len(attribResult) == 1): #if attribution is unique
                    evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_true_positives"] += 1
                evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_correct_in_list"] += 1
            else:
                if(len(attribResult) == 1): #if attribution is unique
                    evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_false_positives"] += 1
                evaluationDictionary[stegoToolIdentifier][attribType][attribName]["_incorrect_in_list"] += 1

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
