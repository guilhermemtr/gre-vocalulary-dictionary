prefix = "  "
suffix = "\n"
majorPrefixKey = "\n"

dictionaryRepresentationSpacingDefinitions = {'letter': 4, 'word': 3, 'ctx-word': 2, 'ctx-word detail': 1}


def getPrefix():
    return prefix

def getSuffix():
    return suffix

def getMajorPrefix(n):
    return n*majorPrefixKey
