from Options import *
from Config import *

import textwrap
from nltk.corpus import wordnet as wn

def getLineString(line, prefix = "", suffix = ""):
    return prefix + line.capitalize() + suffix + getSuffix()

class ContextWord:
    def __init__(self, word, meaning):
        self.word = word
        self.meaning = meaning

    def getWordDescription(self, prefix, options):
        description = getLineString(self.word, prefix)
        descPrefix = prefix + getPrefix()
        if options.getOptions()['definition']:
            description += getLineString(self.meaning.definition(), descPrefix)
        return description

class Word:
    def __init__(self, word):
        self.word = word.capitalize()
        self.meanings = wn.synsets(self.word)
        self.words = []
        for meaning in self.meanings:
            self.words.append(ContextWord(self.word,meaning))
        
    def getContextWords(self):
        return self.words.copy()
    
    def wordDescription(self, prefix, options):
        description = getLineString(self.word, prefix)
        pref = prefix + getPrefix()
        ctxWordCount = 1
        for ctxWord in sorted(self.words):
            if ctxWordCount > 1:
                description += getMajorPrefix(dictionaryRepresentationSpacingDefinitions['ctxWord'])
            description += getLineString("Sense %d" % ctxWordCount, pref)
            description += ctxWord.getWordDescription(pref, options)
            ctxWordCount = ctxWordCount + 1
        return description
