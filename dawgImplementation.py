import string

class Node:
    nodeID = 0

    def __init__(self):
        self.number = Node.nodeID
        Node.nodeID += 1
        self.endsWord = False
        self.neighbors = {}

    # makes a string representation of each Node using children's strings too
    def __str__(self):
        listRepresent = []
        if self.endsWord:
            listRepresent.append("1")
        else:
            listRepresent.append("0")
        for each in self.neighbors.items():
            listRepresent.append(each[0])
            listRepresent.append(str(each[1]))
        return "_".join(listRepresent)

    def __hash__(self):
        return self.__str__().__hash__()

    def __eq__(self, other):
        return self.__str__() == other.__str__()

# Structure that holds nodes
class Dawg:
    def __init__(self):
        self.previousWord = ""
        self.root = Node()
        self.freshNodes = []
        self.trimmedNodes = {}

    def insert(self, word):
        if word < self.previousWord:
            raise Exception("Error: Words not listed alphabetically")
        #find prefix from previous
        numLetterInCommon = 0
        for i in range (min(len(word), len(self.previousWord))):
            if word[i] != self.previousWord[i]:
                break
            numLetterInCommon += 1

        self._removeRedundantNodes(numLetterInCommon)

        #since first part of word already maybe exists, add remainder

        if len(self.freshNodes) == 0:
            #if no freshnodes, tempnode is root
            tempNode = self.root
        else:
            #set tempnode to last freshnode's next node
            tempNode = self.freshNodes[-1][2]

        #every letter not added already goes to freshnodes
        for letter in word[numLetterInCommon:]:
            nextNode = Node()
            tempNode.neighbors[letter] = nextNode
            self.freshNodes.append((tempNode, letter, nextNode))
            tempNode = nextNode

        tempNode.endsWord = True
        self.previousWord = word

    def finish(self):
        #remove all redundant Nodes
        self._removeRedundantNodes(0)

    def _removeRedundantNodes(self, until):
        for i in range (len(self.freshNodes) - 1, until - 1, -1):
            (parent, letter, child) = self.freshNodes[i]
            if child in self.trimmedNodes:
                parent.neighbors[letter] = self.trimmedNodes[child]
            else:
                self.trimmedNodes[child] = child
            self.freshNodes.pop()

    def lookup(self, word, startNode):
        if not startNode:
            startNode = self.root
        word = word.upper()
        node = startNode
        for letter in word:
            if letter not in node.neighbors:
                return False
            node = node.neighbors[letter]
        return node.endsWord

    def lookupEndOptions(self, wordStart):
        wordStart = wordStart.upper()
        node = self.root
        for letter in wordStart:
            if letter not in node.neighbors:
                return False, []
            node = node.neighbors[letter]
        return True, node.neighbors.keys()

    def lookupStartOptions(self, wordEnd):
        wordEnd = wordEnd.upper()
        options = list(string.ascii_uppercase)
        print(options)
        for x in range(len(options) - 1, 0, -1):
            temp = options[x] + wordEnd
            if not self.lookup(temp, None):
                options.pop()
        if len(options) == 0:
            return False, []
        return True, options

    def lookupBoth(self, wordStart, wordEnd):
        wordStart = wordStart.upper()
        node = self.root
        for letter in wordStart:
            if letter not in node.neighbors:
                return False, []
            node = node.neighbors[letter]
        # node now equals node after end of wordStart
        options = list(string.ascii_uppercase)
        finalOptions = []
        for option in options:
            if self.lookup(option + wordEnd, node):
                finalOptions.append(option)
        if len(finalOptions) == 0:
            return False, []
        return True, finalOptions

    def numNodes(self):
        return len(self.trimmedNodes)

    def numEdges(self):
        count = 0
        for node in self.trimmedNodes:
            count += len(node.neighbors)
        return count
