from Options import *
from Config import *

import textwrap
from nltk.corpus import wordnet as wn
from PyDictionary import PyDictionary
import dictcom
import itertools
import math

dictionary=PyDictionary() 

def getLineString(line, prefix = "", suffix = "", extraSuffix = getSuffix()):
    return prefix + line.capitalize().replace("%20", " ").replace("_", " ") + suffix + extraSuffix

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

fieldSeparator = "||"
tagSeparator = ";"
defaultListSeparator = ":"
defaultSeparator = "."

wordPropertyNames = {
    'definition' : "Definition",
    'synonyms'   : "Synonyms",
    'antonyms'   : "Antonyms",
    'examples'   : "Examples",
    'tags'       : "Tags",
}

def standardizedPropertyDescription(prefix, propertyName, valueList = [], suffixSeparator = defaultSeparator, suffix = getSuffix()):
    description = getLineString(propertyName, prefix, defaultListSeparator)
    if len(valueList) == 0:
        description += getLineString("None", prefix, defaultSeparator)
    else:
        missing = len(valueList)
        for value in valueList:
            separator = suffixSeparator
            missing = missing - 1
            if missing == 0:
                separator = defaultSeparator
            description += getLineString(value, prefix + getPrefix('ctx-word detail instance'), separator)
    return description


class ContextWord:
    def __init__(self, meaning, word):
        self.meaning = meaning
        self._word = word

    def word(self):
        return self.meaning.lemmas()[0].name()

    def pos(self):
        return wordType[self.meaning.pos()]()
        
    def getWordDefinition(self, prefix):
        return standardizedPropertyDescription(prefix, wordPropertyNames['definition'], [self.meaning.definition()])
        
    def getWordExamples(self, prefix):
        return standardizedPropertyDescription(prefix, wordPropertyNames['examples'], self.meaning.examples())

    def getWordSynonyms(self, prefix):
        syns = [lemma.name().capitalize() for lemma in self.meaning.lemmas()]
        synonyms = [syn.replace('_', ' ') for syn in syns if syn != self._word]
        return standardizedPropertyDescription(prefix, wordPropertyNames['synonyms'], synonyms)

    def getWordAntonyms(self, prefix):
        ants = [lemma.antonyms() for lemma in self.meaning.lemmas()]
        antonyms = [ant.name().replace('_', ' ') for ant in list(itertools.chain.from_iterable(ants))]
        return standardizedPropertyDescription(prefix, wordPropertyNames['antonyms'], antonyms)
    
    def getWordDescription(self, prefix, options):
        descPrefix = prefix + getPrefix('ctx-word detail')
        description = ""
        if options.getOption('definition'):
            description += getMajorPrefix('ctx-word detail')
            description += self.getWordDefinition(descPrefix)

        if options.getOption('synonyms'):
            description += getMajorPrefix('ctx-word detail')
            description += self.getWordSynonyms(descPrefix)

        if options.getOption('antonyms'):
            description += getMajorPrefix('ctx-word detail')
            description += self.getWordAntonyms(descPrefix)

        if options.getOption('examples'):
            description += getMajorPrefix('ctx-word detail')
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
        try:
            return standardizedPropertyDescription(prefix, wordPropertyNames['definition'], dictionary.meaning(self.word()))
        except:
            return standardizedPropertyDescription(prefix, wordPropertyNames['definition'])
        
    def getWordSynonyms(self, prefix):
        try:
            return standardizedPropertyDescription(prefix, wordPropertyNames['synonyms'], dictionary.synonym(self.word()))
        except:
            return standardizedPropertyDescription(prefix, wordPropertyNames['synonyms'])
        
    def getWordAntonyms(self, prefix):
        try:
            return standardizedPropertyDescription(prefix, wordPropertyNames['antonyms'], dictionary.antonym(self.word()))
        except:
            return standardizedPropertyDescription(prefix, wordPropertyNames['antonyms'])
        
    def getWordExamples(self, prefix):
        return standardizedPropertyDescription(prefix, wordPropertyNames['examples'])


    def getWordDescription(self, prefix, options):
        descPrefix = prefix + getPrefix('ctx-word detail')
        description = ""
        if options.getOption('definition'):
            description += getMajorPrefix('ctx-word detail')
            description += self.getWordDefinition(descPrefix)

        if options.getOption('synonyms'):
            description += getMajorPrefix('ctx-word detail')
            description += self.getWordSynonyms(descPrefix)

        if options.getOption('antonyms'):
            description += getMajorPrefix('ctx-word detail')
            description += self.getWordAntonyms(descPrefix)

        if options.getOption('examples'):
            description += getMajorPrefix('ctx-word detail')
            description += self.getWordExamples(descPrefix)

        return description


class Word:
    def __init__(self, word, level = 0, tags = [""]):
        self.tags = tags
        self.words = []
        self.word = word.capitalize().replace(" ", "_")
        meanings = wn.synsets(self.word)
        self.level = level
        if len(meanings) == 0:
            print ("Not found in NLTK: " + self.word)
            self.word = self.word.replace("_", "%20")
            self.words.append(ThesaurusWord(self.word))
        else:
            for meaning in meanings:
                self.words.append(ContextWord(meaning, self.word))

    def getWord(self):
        return self.word

    def getLevel(self):
        return self.level

    def getTags(self):
        return self.tags
    
    def wordDescription(self, prefix, options):
        description = ""
        if options.getOption('word'):
            description += getLineString(self.word, prefix)
            description += getMajorPrefix('word detail')

        if options.getOption('tags'):
            description += standardizedPropertyDescription(prefix, wordPropertyNames['tags'], self.tags)
        if options.getOption('difficulty'):
            description += getLineString("Difficulty: ", prefix + getPrefix('word detail'), str(self.level))
        ctxWordCount = 1
        for ctxWord in self.words:
            if ctxWordCount > 1:
                if options.getOption('explicit-senses'):
                    description += getMajorPrefix('ctx-word')
            elif options.getOption('difficulty'):
                description += getMajorPrefix('word detail')

            if options.getOption('explicit-senses'):
                description += getLineString("Sense %d, as in %s (%s)" % (ctxWordCount,ctxWord.word(), ctxWord.pos()), prefix + getPrefix('ctx-word'), ":")
            
            description += ctxWord.getWordDescription(prefix + getPrefix('ctx-word'), options)
            ctxWordCount = ctxWordCount + 1
        return description
