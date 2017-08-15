from Options import *
from Config import *

import textwrap
from nltk.corpus import wordnet as wn
from PyDictionary import PyDictionary
import dictcom

dictionary=PyDictionary() 


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

        if options.getOptions()['synonyms']:
            description += self.getWordSynonyms(descPrefix)

        if options.getOptions()['antonyms']:
            description += self.getWordAntonyms(descPrefix)

        if options.getOptions()['examples']:
            description += self.getWordExamples(descPrefix)

        return description

class ThesaurusWord:
    def __init__(self, word):
        self._word = word

    def word(self):
        return self._word

    def pos(self):
        return "expression"
        
    def getWordDefinition(self, prefix):
        definitions = getLineString('Definitions', prefix, ":")
        defCount = 0
        try:
            defs = dictionary.meaning(self._word)
        except:
            defs = None
        if defs != None:
            for definition in defs:
                definitions += getLineString(definition, prefix, ".")
                defCount = defCount + 1
        else:
            definitions += getLineString("No definition available", prefix, ".")
            defCount = 1 #Not trusting that the library returns non empty lists

        if defCount == 0:
            definitions += getLineString("No definition available", prefix, ".")
        
        return definitions

    def getWordSynonyms(self, prefix):
        synonyms = getLineString('Synonyms', prefix, ":")
        synonymCount = 0
        try:
            syn = dictionary.synonym(self._word)
        except:
            syn = None
        if syn != None:
            for synonym in syn:
                synonyms += getLineString(synonym.replace('_', ' '), prefix + getPrefix(), ".")
                synonymCount = synonymCount + 1
        else:
            synonyms += getLineString("No synonyms available", prefix, ".")
            synonymCount = 1

        if synonymCount == 0:
            synonyms += getLineString("No synonyms available", prefix, ".")
        
        
        return synonyms

    def getWordAntonyms(self, prefix):
        antonyms = getLineString('Antonyms', prefix, ":")
        antonymCount = 0
        try:
            ant = dictionary.antonym(self._word)
        except:
            ant = None
            
        if ant != None:
            for antonym in ant:
                antonyms += getLineString(antonym, prefix + getPrefix(), ".")
                antonymCount = antonymCount + 1
        else:
            antonyms += getLineString("No antonyms available", prefix, ".")
            antonymCount = 1
            
        if antonymCount == 0:
            antonyms += getLineString("No antonyms available", prefix, ".")
        return antonyms

    def getWordExamples(self, prefix):
        examples = getLineString('Examples', prefix, ":")
        examples += getLineString("None", prefix, ".")
        return examples


    def getWordDescription(self, prefix, options):
        descPrefix = prefix + getPrefix()
        description = ""
        if options.getOptions()['definition']:
            description += self.getWordDefinition(descPrefix)

        if options.getOptions()['synonyms']:
            description += self.getWordSynonyms(descPrefix)

        if options.getOptions()['antonyms']:
            description += self.getWordAntonyms(descPrefix)

        if options.getOptions()['examples']:
            description += self.getWordExamples(descPrefix)

        return description

    
class Word:
    def __init__(self, word, level = 0):
        self.words = []
        self.word = word.capitalize().replace(" ", "%20")
        self.type = ""
        self.level = level
        if word.capitalize() != self.word:
            self.type = "Thesaurus"
            self.words.append(ThesaurusWord(self.word))
        else:
            self.type = "Nltk"
            meanings = wn.synsets(self.word)
            for meaning in meanings:
                self.words.append(ContextWord(meaning))

    def getWord(self):
        return self.word

    def getLevel(self):
        return self.level
    
    def wordDescription(self, prefix, options):
        description = getLineString(self.word.replace("%20", " "), prefix)
        description += getLineString("Difficulty: ", prefix, str(self.level))
        pref = prefix + getPrefix()
        ctxWordCount = 1
        for ctxWord in self.words:
            if ctxWordCount > 1:
                description += getMajorPrefix(dictionaryRepresentationSpacingDefinitions["ctx-word"])
            description += getLineString("Sense %d, as in %s (%s)" % (ctxWordCount,ctxWord.word().replace("%20", " "), ctxWord.pos()), pref, ":")
            description += ctxWord.getWordDescription(pref, options)
            ctxWordCount = ctxWordCount + 1
        return description
