# Based heavily on Steve Hanov's 2011 DAWG program

import dawgImplementation
import time
import pickle

SOURCE = "wordList.txt"

if __name__ == '__main__':
    dictionary = dawgImplementation.Dawg()
    WordCount = 0
    words = open(SOURCE, "rt").read().split()
    words.sort()
    start = time.time()
    for word in words:
        WordCount += 1
        dictionary.insert(word)
        if ( WordCount % 10000 ) == 0: print(WordCount)
    dictionary.finish()
    print("It took: " + str(time.time() - start))

    EdgeCount = dictionary.numEdges()
    print("Read " + str(WordCount) + " words into " + str(dictionary.numNodes()) + " nodes and " + str(EdgeCount) + " edges")
    print("This could be stored in as little as " + str(EdgeCount * 4) + " bytes")


    pickle.dump( dictionary, open("pickleDict.p", "wb"))

    print("Pickled as pickleDict")
