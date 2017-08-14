import textwrap
from nltk.corpus import wordnet as wn
from Options import *

class ContextWord:
    def __init__(self, word, meaning):
        self.word = word
        self.meaning = meaning

    def definition(self):
        return self.meaning.definition()

class Word:
    def __init__(self, word):
        self.word = word
        self.meanings = wn.synsets(self.word)
        self.words = []
        for meaning in self.meanings:
            self.words.append(ContextWord(self.word,meaning))

    def getWordData(self, definition = True, synonyms = True, antonyms = True, examples = True):
        for word in self.words:
            print(word.definition() + "\n")

