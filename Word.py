from Options import *
from Config import *

import textwrap
from nltk.corpus import wordnet as wn

def getLineString(line, prefix = "", suffix = ""):
    return prefix + line.capitalize() + suffix + getSuffix()

def adj():
    return "adjective"

def adjSat():
    return "satellite adjective"

def adv():
    return "adverb"

def noun():
    return "noun"

def verb():
    return "verb"

wordType = {
            'a' : adj,
            's' : adjSat,
            'r' : adv,
            'n' : noun,
            'v' : verb,
}

class ContextWord:
    def __init__(self, meaning):
        self.meaning = meaning

    def word(self):
        return self.meaning.lemmas()[0].name()

    def pos(self):
        return wordType[self.meaning.pos()]()
        
    def getWordDefinition(self, prefix):
        return getLineString('Definition', prefix, ":") + getLineString(self.meaning.definition(), prefix, ".")

    def getWordExamples(self, prefix):
        examples = getLineString('Examples', prefix, ":")
        for example in self.meaning.examples():
            examples += getLineString(example, prefix + getPrefix(), ".")
        if len(self.meaning.examples()) == 0:
            examples += getLineString("None", prefix, ".")
        return examples

    def getWordSynonyms(self, prefix):
        synonyms = getLineString('Synonyms', prefix, ":")
        for synonym in self.meaning.lemmas():
            syn = synonym.name()
            if syn != self.word():
                synonyms += getLineString(syn.replace('_', ' '), prefix + getPrefix(), ".")
        if len(self.meaning.lemmas()) == 1:
            synonyms += getLineString("None", prefix, ".")
        return synonyms

    def getWordAntonyms(self, prefix):
        antonyms = getLineString('Antonyms', prefix, ":")
        antonymCount = 0
        for synonym in self.meaning.lemmas():
            for antonym in synonym.antonyms():
                antonyms += getLineString(antonym.name().replace('_', ' '), prefix + getPrefix(), ".")
                antonymCount = antonymCount + 1
        if antonymCount == 0:
            antonyms += getLineString("None", prefix, ".")
        return antonyms

    
    def getWordDescription(self, prefix, options):
        descPrefix = prefix + getPrefix()
        description = ""
        if options.getOptions()['definition']:
            description += self.getWordDefinition(descPrefix)
            
        if options.getOptions()['examples']:
            description += self.getWordExamples(descPrefix)

        if options.getOptions()['synonyms']:
            description += self.getWordSynonyms(descPrefix)

        if options.getOptions()['antonyms']:
            description += self.getWordAntonyms(descPrefix)

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
            description += getLineString("Sense %d, as in %s (%s)" % (ctxWordCount,ctxWord.word(), ctxWord.pos()), pref, ":")
            description += ctxWord.getWordDescription(pref, options)
            ctxWordCount = ctxWordCount + 1
        return description
