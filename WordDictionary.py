from Word import *

class WordDictionary:
    def __init__(self, filenames):
        self.words = {}
        for filename in filenames:
            self.loadWordsFromFile(filename)

    def loadWordsFromFile(self, filename):
        f = open(filename, 'r')
        for line in f:
            self.addWord(line.lower().replace("\n",""))
        f.close()

    def saveDictionary(self, filename, options):
        f = open(filename, 'w')
        currentChar = 'A'
        wordCount = 0
        prefix = getPrefix()
        for k in sorted(self.words):
            if k.capitalize()[0] != currentChar or wordCount == 0:
                currentChar = k.capitalize()[0]
                spacing = ""
                if wordCount > 0:
                    spacing = getMajorPrefix(dictionaryRepresentationSpacingDefinitions['letter'])
                f.write(getLineString(currentChar, spacing))
            f.write(self.words[k].wordDescription(prefix, options))
            wordCount = wordCount + 1
        f.close()

    def addWord(self, word):
        self.words[word] = Word(word)

    def deleteWord(self, word):
        del self.words[word]

    def existsWord(self, word):
        return word in self.words

    def getWord(self, word):
        if word in self.words:
            return self.words[word]
        else:
            raise Exception(word + " is not in the dictionary")
        
    def getDictionaryWords(self):
        return self.words.keys
    
