import dawgImplementation
import pickle
import time
import Square



class Board:
    def __init__(self):
        self.boardState = [[Square.Square() for x in range(15)] for y in range(15)]
        #67108863 is bit vector of every letter
        self.adjacentBitVector = [[67108863 for x in range(15)] for y in range(15)]
        self.dictionary = pickle.load(open("pickleDict.p", "rb"))
        self.robotRack = []
        self.moveList = []

    def __str__(self):
        returnString = ""
        for row in self.boardState:
            for unit in row:
                returnString += '|' + str(unit)
            returnString += "|\n"
        return returnString

    def _printAdjacency(self):
        returnString = ""
        for row in self.adjacentBitVector:
            for unit in row:
                value = 0
                if unit != 0:
                    value = 1
                returnString += '|' + str(value)
            returnString += "|\n"
        print(returnString)

    def _printAnchor(self):
        returnString = ""
        for row in self.boardState:
            for unit in row:
                if unit.isAnchor():
                    val = 1
                else:
                    val = 0
                returnString += '|' + str(val)
            returnString += "|\n"
        print(returnString)

    def getBoardState(self):
        return self.boardState

    def addTile(self, letter, row, col):
        if len(letter) == 1 and self.boardState[row][col].isEmpty():
            self.boardState[row][col].add(letter)
        else:
            raise Exception("Tile must be of length 1 and position must be empty")

        self.updateAdjacenyOfTile(row + 1, col)
        self.updateAdjacenyOfTile(row - 1, col)

        self.boardState[row + 1][col].setAnchor()
        self.boardState[row - 1][col].setAnchor()
        self.boardState[row][col + 1].setAnchor()
        self.boardState[row][col - 1].setAnchor()
        changeRow = row

        #if there is a word bellow, follow it and update the adj of the closest free space
        if self.boardState[changeRow + 1][col].isNotEmpty():
            while changeRow < 14:
                changeRow += 1
                if self.boardState[changeRow + 1][col].isEmpty():
                    self.updateAdjacenyOfTile(changeRow + 1, col)
                    break
        #if there is a word above, follow it and update the adj of the closest free space
        changeRow = row
        if self.boardState[changeRow - 1][col].isNotEmpty():
            while changeRow > 0:
                changeRow -= 1
                if self.boardState[changeRow - 1][col].isEmpty():
                    self.updateAdjacenyOfTile(changeRow - 1, col)
                    break

    def updateAdjacenyOfTile(self, row, col):
        options = []
        #if tile immediately above and below filled
        if row > 0 and self.boardState[row - 1][col].isNotEmpty() and row < 14 and self.boardState[row + 1][col].isNotEmpty():
            wordStart = self._findWordStart(row - 1, col, 1)
            wordEnd = self._findWordStart(row + 1, col, 3)
            hasBothOptions = self.dictionary.lookupBoth(wordStart, wordEnd)
            if hasBothOptions[0]:
                options += hasBothOptions[1]

        else:
            #just tile above
            if row > 0 and self.boardState[row - 1][col].isNotEmpty():
                wordStart = self._findWordStart(row - 1, col, 1)
                hasUps = self.dictionary.lookupEndOptions(wordStart)
                if hasUps[0]:
                    options += hasUps[1]
            #just tile below
            if row < 14 and self.boardState[row + 1][col].isNotEmpty():
                wordEnd = self._findWordStart(row + 1, col, 3)
                hasDowns = self.dictionary.lookupStartOptions(wordEnd)
                if hasDowns[0]:
                    options += hasDowns[1]
        value = 0
        print("options: " + str(options))
        for option in options:
            tempVal = ord(option) - ord('A')
            if tempVal >= 0 and tempVal < 26:
                num = 1 << tempVal
            value = value | num
        self.adjacentBitVector[row][col] = value



    #direction should be 1,2,3,4
    #assumes row, col given is legitimate start to word
    def _findWordStart(self, row, col, direction):
        wordStart = ""
        wordStart += self.boardState[row][col].get()
        if direction == 1:
            #up
            while row > 0 and self.boardState[row - 1][col].isNotEmpty():
                wordStart = self.boardState[row - 1][col].get() + wordStart
                row -= 1
        elif direction == 2:
            #right
            while col < 14 and self.boardState[row][col + 1].isNotEmpty():
                wordStart += self.boardState[row][col + 1].get()
                col += 1
        elif direction == 3:
            #down
            while row < 14 and self.boardState[row + 1][col].isNotEmpty():
                wordStart += self.boardState[row + 1][col].get()
                row += 1
        elif direction == 4:
            #left
            while col > 0 and self.boardState[row][col - 1].isNotEmpty():
                wordStart = self.boardState[row][col - 1].get() + wordStart
                col -= 1
        else:
            return ""
        return wordStart

    def _bitVectorToList(self, value):
        offset = 0
        result = []
        while value != 0:
            if(value & 1 != 0):
                temp = offset + ord('A')
                result.append(chr(temp))
            value = value & ~1
            value = value >> 1
            offset += 1
        return result

    def listPlays(self):
        self.moveList.clear()
        for rowIndex in range(len(self.boardState)):
            k = 0
            for colIndex in range(len(self.boardState[0])):
                if self.boardState[rowIndex][colIndex].isAnchor():
                    if colIndex > 0 and self.boardState[rowIndex][colIndex - 1].isNotEmpty():
                        iterNode = self.dictionary.root
                        wordStart = self._findWordStart(rowIndex, colIndex, 4)
                        for l in wordStart:
                            if l not in iterNode.neighbors:
                                raise Exception("Illegal word on board")
                            iterNode = iterNode.neighbors[l]
                            print("It be: " + l)
                        self.extendRight(wordStart, iterNode, rowIndex, colIndex)
                    else:
                        self.leftPart("", self.dictionary.root, k, rowIndex, colIndex)
                        print(k)
                    k = 0

                else:
                    k += 1

    def crossCheckContains(self, letter, row, col):
        value = self.adjacentBitVector[row][col]
        shiftAmount = ord(letter) - ord('A')
        if ((1 << shiftAmount) & value) != 0:
            #in bit vector
            return True
        return False

    def extendRight(self, partialWord, node, row, col):
        if row > 14:
            return
        if self.boardState[row][col].isEmpty():
            if node.endsWord:
                #found legal move
                self.moveList.append(partialWord)
            for e in node.neighbors:
                if e in self.robotRack and self.crossCheckContains(e, row, col):
                    self.robotRack.remove(e)
                    self.extendRight(partialWord + e, node.neighbors[e], row, col + 1)
                    self.robotRack.append(e)
        else:
            if self.boardState[row][col].get() in node.neighbors:
                self.extendRight(partialWord + self.boardState[row][col].get(), node.neighbors[self.boardState[row][col].get()], row, col + 1)

    def leftPart(self, partialWord, node, limit, row, col):
        self.extendRight(partialWord, node, row, col)
        if limit > 0:
            for e in node.neighbors:
                if e in self.robotRack:
                    self.robotRack.remove(e)
                    self.leftPart(partialWord + e, node.neighbors[e], limit - 1, row, col)
                    self.robotRack.append(e)

if __name__ == '__main__':

    game = Board()
    game.addTile('T', 2, 4)
    game.addTile('U', 2, 5)
    game.addTile('N', 2, 6)
    game.addTile('A', 2, 7)
    print(game)
    game.robotRack = ['F', 'I', 'S', 'H']
    game.listPlays()
    print(game.moveList)




    #print(game.test("bike"))
