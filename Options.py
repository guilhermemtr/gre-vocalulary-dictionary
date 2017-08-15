class Options:
    def __init__(self, level = 0, definition = True, synonyms = True, antonyms = True, examples = True):
        self.options = {"level": 0, "definition": definition, "synonyms" : synonyms, "antonyms" : antonyms, "examples" : examples}

    def getOptions(self):
        return self.options
    
