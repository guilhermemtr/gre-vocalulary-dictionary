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
        words = []
        for k,v in self.words.items():
            words.append(k)
        return words
            

