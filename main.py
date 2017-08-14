#!/usr/bin/python
# Python version: 3.6.2



import sys
import textwrap
from nltk.corpus import wordnet as wn


POS = {
    'v': 'verb',
    'a': 'adjective',
    's': 'satellite adjective', 
    'n': 'noun', 'r': 'adverb'
}

options = {'inputFiles' : [], 'outputFile': "", 'meaning' : True, 'synonyms': True, 'antonyms': True, 'examples': True}

class Word:
    word = ""
    definition = ""
    synonyms = []
    antonyms = []
    examples = []
    

wordDictionary = {}


# debugging functions
def showArguments():
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))

def getWordsFromFile(fn):
    f = open(fn, 'r')
    words = []
    for line in f:
        words.append(line.lower().replace("\n",""))
    return words

def writeLinesToFile(fn, words):
    f = open(fn, 'w')
    for word in words:
        words.append(line.lower().replace("\n",""))
    return words

def main():
    # my code here
    showArguments()
    print(getWordsFromFile("input"))




if __name__ == "__main__":
    main()
