class Options:
    def __init__(self, definition = True, synonyms = True, antonyms = True, examples = True):
        self.options = {"definition": definition, "synonyms" : synonyms, "antonyms" : antonyms, "examples" : examples}

    def getOptions(self):
        return self.options
    
