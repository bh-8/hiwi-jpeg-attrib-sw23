def evaluate(attribName, attribValue):
    match attribName:
        case "jfifVersion":
            return ["jsteg"] if attribValue == None else []
        case "binwalkData":
            return ["jsteg"] if attribValue == None else []
        case "fileHeader":
            if not attribValue == None:
                if not "JFIF" in attribValue:
                    return ["jsteg"]
                if "((((((((((((((((((((((((((((((((((((((((((((((((((" in attribValue:
                    return ["f5"]
                if "56789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz" not in attribValue:
                    return ["jphide"]
                if "!22222222222222222222222222222222222222222222222222" in attribValue and not "Exif" in attribValue:
                    return ["outguess", "steghide"] #TODO: not clear: subject to validate!
            return []
        case "foremostCarving":
            return ["jsteg"] if attribValue == None else []
        case "fileSize":
            commaSplit = list(map(str.strip, attribValue.split(",")))
            stegoSize = int(commaSplit[0].split(":")[1].strip())
            originalSize = int(commaSplit[1].split(":")[1].strip())
            differenceSize = int(commaSplit[2].split(":")[1].strip())

            #TODO: and: more conservative, or: more aggressive
            if differenceSize < originalSize / 2 and stegoSize > originalSize / 2:
                return ["jphide", "steghide"]
            return []
        case "colorMeanDifference":
            commaSplit = list(map(str.strip, attribValue.split(",")))

            if commaSplit[0] != "None" and commaSplit[1] != "None" and commaSplit[2] != "None" and commaSplit[3] != "None":
                colorMean = float(commaSplit[0].split(" ")[1])
                colorMeanR = float(commaSplit[1].split(" ")[1])
                colorMeanG = float(commaSplit[2].split(" ")[1])
                colorMeanB = float(commaSplit[3].split(" ")[1])

                colorMeanMean = (colorMeanR + colorMeanG + colorMeanB) / 3

                if colorMean > 127 and colorMean > colorMeanMean - 2.56 and colorMean < colorMeanMean + 2.56:
                    return ["jphide", "steghide"]
            return []
