import dawgImplementation
import pickle
import time
import Square



class Board:
    def __init__(self):
        self.boardState = [[Square.Square() for x in range(15)] for y in range(15)]
        self.adjacentBitVector = [[0 for x in range(15)] for y in range(15)]
        self.dictionary = pickle.load(open("pickleDict.p", "rb"))

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

    def getBoardState(self):
        return self.boardState

    def addTile(self, letter, row, col):
        if len(letter) == 1 and self.boardState[row][col].isEmpty():
            self.boardState[row][col].add(letter)
        else:
            raise Exception("Tile must be of length 1 and position must be empty")
        self.updateAdjacenyOfTile(row + 1, col)
        self.updateAdjacenyOfTile(row - 1, col)


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
        for option in options:
            tempVal = ord(option) - ord('A')
            if tempVal >= 0 and tempVal < 26:
                num = 1 << tempVal
            value = value | num
        self.adjacentBitVector[row][col] = value
        print(str(value) + " row, col: " + str(row) + " " + str(col) )



    #direction should be 1,2,3,4
    #assumes row, col given is legitimate start to word
    def _findWordStart(self, row, col, direction):
        wordStart = ""
        wordStart += self.boardState[row][col].get()
        if direction == 1:
            #up
            while row > 0 and self.boardState[row - 1][col].get() != " ":
                wordStart = self.boardState[row - 1][col].get() + wordStart
                row -= 1
        elif direction == 2:
            #right
            while col < 14 and self.boardState[row][col + 1].get() != " ":
                wordStart += self.boardState[row][col + 1].get()
                col += 1
        elif direction == 3:
            #down
            while row < 14 and self.boardState[row + 1][col].get() != " ":
                wordStart += self.boardState[row + 1][col].get()
                row += 1
        elif direction == 4:
            #left
            while col > 0 and self.boardState[row][col - 1].get() != " ":
                wordStart = self.boardState[row][col - 1].get() + wordStart
                col -= 1
        else:
            return ""
        return wordStart

    def test(self):
        print("bruh")

if __name__ == '__main__':

    game = Board()
    game.addTile('A', 2, 4)
    #game.addTile('Y', 3, 4)
    game.addTile('O', 3, 5)
    game.addTile('E', 4, 4)
    print(game)
    game._printAdjacency()

    #print(game.test("bike"))
