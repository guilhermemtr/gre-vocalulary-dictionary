#!/usr/bin/python
# Python version: 3.6.2

import sys

from WordDictionary import *


# options = {'inputFiles' : [], 'outputFile': "", 'meaning' : True, 'synonyms': True, 'antonyms': True, 'examples': True}



POS = {
    'v': 'verb',
    'a': 'adjective',
    's': 'satellite adjective', 
    'n': 'noun',
    'r': 'adverb'
}


        
    



# debugging functions
def showArguments():
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))

def main():
    options = Options()
    wordDictionary = WordDictionary(["input"])
    wordDictionary.saveDictionary("output", options)
    wordDictionary.saveDictionaryWords("words-indexed")

if __name__ == "__main__":
    main()
