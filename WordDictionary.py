from Word import *


class WordDictionary:
    def __init__(self, filenames, tagListFilename):
        self.longestWord = "" #Only has to be at least the length of the longest word
                              #But it is not necessary that it actually is the longest
        self.maxLevel = 0
        self.words = {}
        self.tags = {}
        self.longestTag = ""
        self.longestTagName = ""
        self.loadTagsFromFile(tagListFilename)
        for filename in filenames:
            self.loadWordsFromFile(filename)

    def loadWordsFromFile(self, filename):
        f = open(filename, 'r')
        for line in f:
            wordData = list(map(str.strip,line.lower().strip().replace("\n","").capitalize().split(fieldSeparator)))
            wlen = len(wordData)
            if   wlen == 3:
                tagNames = [tn for tn in list(map(str.strip, wordData[2].split(tagSeparator))) if tn != ""]
                existingTagNames = [tn for tn in tagNames if tn in self.tags]
                tags = [self.tags[tn] for tn in existingTagNames]
                self.addWord(wordData[0], int(wordData[1]), tags)
            elif wlen == 2:
                self.addWord(wordData[0], int(wordData[1]))
            else:
                self.addWord(wordData[0])
        f.close()

    def loadTagsFromFile(self, filename):
        f = open(filename, 'r')
        for line in f:
            tagData = list(map(str.strip,line.strip().replace("\n","").split(fieldSeparator)))
            self.addTag(tagData[0], tagData[1], tagData[2])
        f.close()

    def storeTagsToFile(self, filename):
        f = open(filename, 'w')
        for tag in sorted(self.tags):
            line = fieldSeparator.join([self.tags[tag].getId(), self.tags[tag].getName(), self.tags[tag].getDesc()])
            f.write(getLineString(line))
        f.close()
        
    def saveDictionary(self, filename, options):
        f = open(filename, 'w')
        currentChar = 'A'
        wordCount = 0
        spaced = True
        prefix = getPrefix('letter')
        spacing = ""
        for k in sorted(self.words):
            if not (options.getOption('levelFilter'))(self.words[k].getLevel()):
                continue
            if not (options.getOption('tagFilter'))(self.words[k].getTags()):
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

            tags = [tag.getId() for tag in word.getTags()]
            
            wordLine  = word.getWord() + ((wordPadding + 4) * " ")
            wordLine += fieldSeparator + (" " * 4) + lvl + (" " * lvlPadding) + (" " * 4)
            wordLine += fieldSeparator + (" " * 4) + tagSeparator.join(tags) + (" " * 4)
            f.write(getLineString(wordLine))
        f.close()

    def addTag(self, tagId, tagName, tagDesc):
        self.tags[tagId] = Tag(tagId, tagName, tagDesc)
        if len(tagId) > len(self.longestTag):
            self.longestTag = tagId
        if len(tagName) > len(self.longestTagName):
            self.longestTagName = tagName
        
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
    
