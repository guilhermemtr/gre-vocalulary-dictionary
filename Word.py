from Options import *
from Config import *

import textwrap
from nltk.corpus import wordnet as wn

def getLineString(prefix, line):
    return prefix + line + "\n"

class ContextWord:
    def __init__(self, word, meaning):
        self.word = word
        self.meaning = meaning

    def definition(self):
        return self.meaning.definition()

    def storeContextWordOnFile(self, f, prefix, options):
        ctxPrefix = prefix + "\t"
        f.write(self.getWordDescription(ctxPrefix, options))

    def getWordDescription(self, prefix, options):
        description = getLineString(prefix, self.word)
        descPrefix = prefix + getPrefix()
        if options['definition']:
            description += getLineString(descPrefix, self.meaning.definition())
        
            

class Word:
    def __init__(self, word):
        self.word = word
        self.meanings = wn.synsets(self.word)
        self.words = []
        for meaning in self.meanings:
            self.words.append(ContextWord(self.word,meaning))

    def storeWordInFile(self, f, prefix, options):
        for word in self.words:
            word.storeContextWordOnFile(f, options)
        
    def getWordData(self, options):
        for word in self.words:
            print(word.definition() + "\n")

