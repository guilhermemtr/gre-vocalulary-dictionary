class Options:
    def __init__(self, level = 0, word = True, explicitSenses = True, definition = True, synonyms = True, antonyms = True, examples = True, tags = True, difficulty = True):
        self.options = {"level": 0, "word": word, "explicit-senses": explicitSenses, "definition": definition, "synonyms" : synonyms, "antonyms" : antonyms, "examples" : examples, "tags": tags, "difficulty": difficulty}

    def getOptions(self):
        return self.options
    

    def getOption(self, key):
        return self.options[key]
