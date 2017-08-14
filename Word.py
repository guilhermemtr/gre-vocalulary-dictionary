from Options import *
from Config import *

import textwrap
from nltk.corpus import wordnet as wn

def getLineString(line, prefix = "", suffix = ""):
    return prefix + line.capitalize() + suffix + getSuffix()

class ContextWord:
    def __init__(self, meaning):
        self.meaning = meaning

    def word(self):
        return self.meaning.lemmas()[0].name()

    def getWordDefinition(self, prefix):
        return getLineString('Definition', prefix, ":") + getLineString(self.meaning.definition(), prefix, ".")

    def getWordExamples(self, prefix):
        examples = getLineString('Examples', prefix, ":")
        for example in self.meaning.examples():
            examples += getLineString(example, prefix + getPrefix(), ".")
        if len(self.meaning.examples()) == 0:
            examples += getLineString("None", prefix, ".")
        return examples

    def getWordLemmas(self):
        return meaning.lemmas()

    def getWordSynonymLemmas(self):
        return self.meaning.lemmas()
        
    def getWordSynonyms(self, prefix):
        synonyms = getLineString('Synonyms', prefix, ":")
        for synonym in self.meaning.lemmas():
            syn = synonym.name()
            if syn != self.word():
                synonyms += getLineString(syn, prefix + getPrefix(), ".")
        if len(self.meaning.lemmas()) == 1:
            synonyms += getLineString("None", prefix, ".")
        return synonyms

    
    def getWordDescription(self, prefix, options):
        descPrefix = prefix + getPrefix()
        description = ""
        if options.getOptions()['definition']:
            description += self.getWordDefinition(descPrefix)
            
        if options.getOptions()['examples']:
            description += self.getWordExamples(descPrefix)

        if options.getOptions()['synonyms']:
            description += self.getWordSynonyms(descPrefix)
        return description

class Word:
    def __init__(self, word):
        self.word = word.capitalize()
        self.meanings = wn.synsets(self.word)
        self.words = []
        for meaning in self.meanings:
            self.words.append(ContextWord(meaning))
        
    def getContextWords(self):
        return self.words.copy()
    
    def wordDescription(self, prefix, options):
        description = getLineString(self.word, prefix)
        pref = prefix + getPrefix()
        ctxWordCount = 1
        for ctxWord in self.words:
            if ctxWordCount > 1:
                description += getMajorPrefix(dictionaryRepresentationSpacingDefinitions["ctx-word"])
            description += getLineString("Sense %d, as in %s" % (ctxWordCount,ctxWord.word()), pref, ":")
            description += ctxWord.getWordDescription(pref, options)
            ctxWordCount = ctxWordCount + 1
        return description
