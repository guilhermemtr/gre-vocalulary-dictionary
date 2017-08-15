from Word import *

class WordDictionary:
    def __init__(self, filenames):
        self.longestWord = "" #Only has to be at least the length of the longest word
                              #But it is not necessary that it actually is the longest
        self.words = {}
        for filename in filenames:
            self.loadWordsFromFile(filename)

    def loadWordsFromFile(self, filename):
        f = open(filename, 'r')
        for line in f:
            wordData = list(map(str.strip,line.lower().strip().replace("\n","").capitalize().split("||")))
            if len(wordData) > 1:
                self.addWord(wordData[0],int(wordData[1]))
            else:
                self.addWord(wordData[0])
        f.close()

    def saveDictionary(self, filename, options):
        f = open(filename, 'w')
        currentChar = 'A'
        wordCount = 0
        spaced = True
        prefix = getPrefix('letter')
        spacing = ""
        for k in sorted(self.words):
            if self.words[k].getLevel() < options.getOption('level'):
                continue
            if k.capitalize()[0] != currentChar:
                currentChar = k.capitalize()[0]
                if wordCount > 0:
                    spacing = getMajorPrefix('letter')
                    spaced = True
                f.write(spacing)
                f.write(getLineString(currentChar, prefix))
            if not spaced:
                spacing = getMajorPrefix('word')
            else:
                spacing = ""
            f.write(spacing)
            f.write(self.words[k].wordDescription(prefix + getPrefix('word'), options))
            wordCount = wordCount + 1
            spaced = False
        f.close()

    def saveDictionaryWords(self, filename):
        f = open(filename, 'w')
        for k in sorted(self.words):
            word = self.words[k]
            wordString = word.getWord().replace("%20", " ")
            wordPadding = len(self.longestWord) - len(wordString)
            f.write(getLineString(word.getWord().replace("%20", " "), "", ((wordPadding + 4) * " ") +  "||" + (" " * 4) + str(word.getLevel())))
        f.close()

    def updateLongestWord(self, word):
        if len(word) > len(self.longestWord):
            self.longestWord = word
    
    def addWord(self, word):
        self.words[word] = Word(word)
        self.updateLongestWord(word)
        
    def addWord(self, word, level):
        self.words[word] = Word(word, level)
        self.updateLongestWord(word)

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
        return sorted(self.words.keys)
    
