import dawgImplementation
import pickle
import time



class Board:
    def __init__(self):
        self.boardState = [[" " for x in range(15)] for y in range(15)]
        self.adjacentBitVector = [[0 for x in range(15)] for y in range(15)]
        self.dictionary = pickle.load(open("pickleDict.p", "rb"))

    def __str__(self):
        returnString = ""
        for row in self.boardState:
            returnString += '|' + '|'.join(row) + "|\n"
        return returnString

    def getBoardState(self):
        return self.boardState

    def addTile(self, letter, row, col):
        if len(letter) == 1:
            self.boardState[row][col] = letter
        else:
            raise Exception("Attempted to add Tile longer than 1 letter")

    def updateAdjacenyOfTile(self, row, col):
        options = []
        if row > 0 and self.boardState[row - 1][col] != " ":
            wordStart = self._findWordStart(row - 1, col, 1)
            hasUps = self.dictionary.lookupEndOptions(wordStart)
            if hasUps[0]:
                options += hasUps[1]
        if row < 14 and self.boardState[row + 1][col] != " ":
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
        print(value)



    #direction should be 1,2,3,4
    #assumes row, col given is legitimate start to word
    def _findWordStart(self, row, col, direction):
        wordStart = ""
        wordStart += self.boardState[row][col]
        if direction == 1:
            #up
            while row > 0 and self.boardState[row - 1][col] != " ":
                wordStart = self.boardState[row - 1][col] + wordStart
                row -= 1
        elif direction == 2:
            #right
            while col < 14 and self.boardState[row][col + 1] != " ":
                wordStart += self.boardState[row][col + 1]
                col += 1
        elif direction == 3:
            #down
            while row < 14 and self.boardState[row + 1][col] != " ":
                wordStart += self.boardState[row + 1][col]
                row += 1
        elif direction == 4:
            #left
            while col > 0 and self.boardState[row][col - 1] != " ":
                wordStart = self.boardState[row][col - 1] + wordStart
                col -= 1
        else:
            return ""
        return wordStart

    def test(self, word):
        return self.dictionary.lookupOptions(word)

if __name__ == '__main__':

    game = Board()
    game.addTile('A', 2, 4)
    game.addTile('Y', 3, 4)
    game.addTile('O', 3, 5)
    game.addTile('E', 4, 4)
    print(game)
    game.updateAdjacenyOfTile(5, 4)
    #print(game.test("bike"))
