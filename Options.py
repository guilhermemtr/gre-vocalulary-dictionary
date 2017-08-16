def defaultTagFilter(tag):
    return True

def defaultLevelFilter(lvl):
    return True

class Options:
    def __init__(self, tagFilter = defaultTagFilter, levelFilter = defaultLevelFilter, word = True, explicitSenses = True, definition = True, synonyms = True, antonyms = True, examples = True, tags = True, difficulty = True):
        self.options = {"word": word, "explicit-senses": explicitSenses, "definition": definition, "synonyms" : synonyms, "antonyms" : antonyms, "examples" : examples, "tags": tags, "difficulty": difficulty, "tagFilter": tagFilter, "levelFilter": levelFilter}

    def getOptions(self):
        return self.options
    

    def getOption(self, key):
        return self.options[key]
