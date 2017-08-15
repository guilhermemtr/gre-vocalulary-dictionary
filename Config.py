prefix = "  "
suffix = "\n"
majorPrefixKey = "\n"

horizontal = 'h'
vertical = 'v'

dictionaryRepresentationSpacings = {
    'letter':
    {
        horizontal: 0,
        vertical: 6,
    },
    'word':
    {
        horizontal: 2,
        vertical: 3,
    },
    'ctx-word':
    {
        horizontal: 2,
        vertical: 1,
    },
    'word detail':
    {
        horizontal: 1,
        vertical: 0,
    },
    'ctx-word detail':
    {
        horizontal: 1,
        vertical: 0,
    },
    'ctx-word detail instance':
    {
        horizontal: 2,
        vertical: 0,
    },
}

def getVerticalSpacing(key):
    return dictionaryRepresentationSpacings[key][vertical]

def getHorizontalSpacing(key):
    return dictionaryRepresentationSpacings[key][horizontal]

def getPrefix(key):
    return getHorizontalSpacing(key)*prefix

def getMajorPrefix(key):
    return getVerticalSpacing(key)*majorPrefixKey

def getSuffix():
    return suffix
