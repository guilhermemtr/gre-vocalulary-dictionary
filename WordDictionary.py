from Word import *


class WordDictionary:
    def __init__(self, filenames):
        self.longestWord = "" #Only has to be at least the length of the longest word
                              #But it is not necessary that it actually is the longest
        self.maxLevel = 0
        self.words = {}
        for filename in filenames:
            self.loadWordsFromFile(filename)

    def loadWordsFromFile(self, filename):
        f = open(filename, 'r')
        for line in f:
            wordData = list(map(str.strip,line.lower().strip().replace("\n","").capitalize().split(fieldSeparator)))
            wlen = len(wordData)
            if   wlen == 3:
                tags = [s for s in list(map(str.strip, wordData[2].split(tagSeparator))) if s != ""]
                self.addWord(wordData[0], int(wordData[1]), tags)
            elif wlen == 2:
                self.addWord(wordData[0], int(wordData[1]))
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
            if k.capitalize()[0] != currentChar or wordCount == 0:
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
            
            lvl = str(word.getLevel())
            lvlPadding = len(str(self.maxLevel)) - len(lvl)

            tags = word.getTags()
            
            wordLine  = word.getWord() + ((wordPadding + 4) * " ")
            wordLine += fieldSeparator + (" " * 4) + lvl + (" " * lvlPadding) + (" " * 4)
            wordLine += fieldSeparator + (" " * 4) + tagSeparator.join(tags) + (" " * 4)
            f.write(getLineString(wordLine))
        f.close()
            
    def addWord(self, word, level = 0, tags = []):
        self.words[word] = Word(word, level, tags)
        if len(word) > len(self.longestWord):
            self.longestWord = word
        self.maxLevel = max(self.maxLevel, level)

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
    
