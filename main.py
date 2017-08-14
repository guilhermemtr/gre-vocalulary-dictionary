#!/usr/bin/python
# Python version: 3.6.2

import sys

from WordDictionary import *


options = {'inputFiles' : [], 'outputFile': "", 'meaning' : True, 'synonyms': True, 'antonyms': True, 'examples': True}



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

def writeLinesToFile(fn, words):
    f = open(fn, 'w')
    for word in words:
        words.append(line.lower().replace("\n",""))
    return words

def main():
    # my code here
    showArguments()
    options = Options()
    wordDictionary = WordDictionary(["input"])
    words = wordDictionary.getDictionaryWords()
    print (words)


if __name__ == "__main__":
    main()
