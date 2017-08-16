#!/usr/bin/python
# Python version: 3.6.2

import sys
from WordDictionary import *


# debugging functions
def showArguments():
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))

def tagFilter(tagObjectList):
    tags = [tag.getId() for tag in tagObjectList]
    return ("!known" in tags) or ("gre" in tags)
    
def main():
    options = Options(tagFilter)
    wordDictionary = WordDictionary(["input"], "input-tags")
    wordDictionary.saveDictionary("output", options)
    wordDictionary.saveDictionaryWords("words-indexed")
    wordDictionary.storeTagsToFile("tags-indexed")

if __name__ == "__main__":
    main()
