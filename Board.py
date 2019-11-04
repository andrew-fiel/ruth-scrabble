import dawgImplementation
import Move
import Square
import pickle
import Score
import copy



class Board:
    def __init__(self):
        self.boardState = [[Square.Square() for x in range(15)] for y in range(15)]
        #Place x of pink Double Word score
        for row in range(15):
            for col in range(15):
                if row == col:
                    self.boardState[row][col].special = "DW"
                if 14 - col == row:
                    self.boardState[row][col].special = "DW"
        #Place the rest manually because weird patterns
        self.boardState[0][0].special = "TW"
        self.boardState[0][7].special = "TW"
        self.boardState[0][14].special = "TW"
        self.boardState[7][0].special = "TW"
        self.boardState[7][14].special = "TW"
        self.boardState[14][0].special = "TW"
        self.boardState[14][7].special = "TW"
        self.boardState[14][14].special = "TW"

        self.boardState[0][3].special = "DL"
        self.boardState[0][11].special = "DL"
        self.boardState[2][6].special = "DL"
        self.boardState[2][8].special = "DL"
        self.boardState[3][0].special = "DL"
        self.boardState[3][7].special = "DL"
        self.boardState[3][14].special = "DL"
        self.boardState[6][2].special = "DL"
        self.boardState[6][6].special = "DL"
        self.boardState[6][8].special = "DL"
        self.boardState[6][12].special = "DL"
        self.boardState[7][3].special = "DL"
        self.boardState[7][11].special = "DL"
        self.boardState[8][2].special = "DL"
        self.boardState[8][6].special = "DL"
        self.boardState[8][8].special = "DL"
        self.boardState[8][12].special = "DL"
        self.boardState[11][0].special = "DL"
        self.boardState[11][7].special = "DL"
        self.boardState[11][14].special = "DL"
        self.boardState[12][6].special = "DL"
        self.boardState[12][8].special = "DL"
        self.boardState[14][3].special = "DL"
        self.boardState[14][11].special = "DL"

        self.boardState[1][5].special = "TL"
        self.boardState[1][9].special = "TL"
        self.boardState[5][1].special = "TL"
        self.boardState[5][5].special = "TL"
        self.boardState[5][9].special = "TL"
        self.boardState[5][13].special = "TL"
        self.boardState[9][1].special = "TL"
        self.boardState[9][5].special = "TL"
        self.boardState[9][9].special = "TL"
        self.boardState[9][13].special = "TL"
        self.boardState[13][5].special = "TL"
        self.boardState[13][9].special = "TL"

        #enable first play of the game
        #self.boardState[7][7].setAnchor()

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
                if unit != 67108863:
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

    def _printSpecial(self):
        returnString = ""
        for row in self.boardState:
            for unit in row:
                returnString += '|' + unit.special
            returnString += "|\n"
        print(returnString)

    def reset(self):
        for row in range(15):
            for col in range(15):
                self.adjacentBitVector[row][col] = 67108863
                self.boardState[row][col].letter = ""
                self.boardState[row][col].anchor = False
                self.boardState[row][col].sideScore = 0
        self.robotRack = []
        self.moveList = []


    def getBoardState(self):
        return self.boardState

    def addTile(self, letter, row, col):
        if len(letter) == 1 and self.boardState[row][col].isEmpty():
            self.boardState[row][col].add(letter)
        else:
            raise Exception("Tile must be of length 1 and position must be empty")

        if row + 1 < 15:
            self.updateAdjacenyOfTile(row + 1, col)
        if row - 1 >= 0:
            self.updateAdjacenyOfTile(row - 1, col)

        if row < 14 and self.boardState[row + 1][col].isEmpty():
            self.boardState[row + 1][col].setAnchor()
        if row > 0 and self.boardState[row - 1][col].isEmpty():
            self.boardState[row - 1][col].setAnchor()
        if col < 14 and self.boardState[row][col + 1].isEmpty():
            self.boardState[row][col + 1].setAnchor()
        if col > 0 and self.boardState[row][col - 1].isEmpty():
            self.boardState[row][col - 1].setAnchor()
        changeRow = row

        #if there is a word bellow, follow it and update the adj of the closest free space
        if changeRow + 1 < 15 and self.boardState[changeRow + 1][col].isNotEmpty():
            while changeRow < 13:
                changeRow += 1
                if self.boardState[changeRow + 1][col].isEmpty():
                    self.updateAdjacenyOfTile(changeRow + 1, col)
                    break
        #if there is a word above, follow it and update the adj of the closest free space
        changeRow = row
        if changeRow - 1 >= 0 and self.boardState[changeRow - 1][col].isNotEmpty():
            while changeRow > 1:
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
            #set values used for scoring later
            self.boardState[row][col].sideScore = self.wordToScore(wordStart)
            self.boardState[row][col].sideScore += self.wordToScore(wordEnd)
            if hasBothOptions[0]:
                options += hasBothOptions[1]

        else:
            #just tile above
            if row > 0 and row < 15 and self.boardState[row - 1][col].isNotEmpty():
                wordStart = self._findWordStart(row - 1, col, 1)
                hasUps = self.dictionary.lookupEndOptions(wordStart)
                self.boardState[row][col].sideScore = self.wordToScore(wordStart)
                if hasUps[0]:
                    options += hasUps[1]
            #just tile below
            if row < 14 and row >= 0 and self.boardState[row + 1][col].isNotEmpty():
                wordEnd = self._findWordStart(row + 1, col, 3)
                hasDowns = self.dictionary.lookupStartOptions(wordEnd)
                self.boardState[row][col].sideScore = self.wordToScore(wordEnd)
                if hasDowns[0]:
                    options += hasDowns[1]
        value = 0
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
                    score = Score.Score()
                    #case anchor immediately right of extant letter
                    if colIndex > 0 and self.boardState[rowIndex][colIndex - 1].isNotEmpty():
                        iterNode = self.dictionary.root
                        # 4 means look left
                        wordStart = self._findWordStart(rowIndex, colIndex, 4)
                        for x in range(colIndex - len(wordStart), colIndex):
                            currentSquare = self.boardState[rowIndex][x]
                            if currentSquare.get() not in iterNode.neighbors:
                                raise Exception("Illegal word on board")
                            iterNode = iterNode.neighbors[currentSquare.get()]
                            adding = self.wordToScore(currentSquare.get())
                            score.word += adding
                        self.extendRight(wordStart, iterNode, rowIndex, colIndex, True, score)
                    else:
                        self.leftPart("", self.dictionary.root, k, rowIndex, colIndex, score)
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

    def wordToScore(self, word):
        sum = 0
        valueDict = {
            '?': 0,
            'E': 1, 'A': 1, 'I': 1, 'O': 1, 'N': 1, 'R': 1, 'T': 1, 'L': 1, 'S': 1, 'U': 1,
            'D': 2, 'G': 2,
            'B': 3, 'C': 3, 'M': 3, 'P': 3,
            'F': 4, 'H': 4, 'V': 4, 'W': 4, 'Y': 4,
            'K': 5,
            'J': 8, 'X': 8,
            'Q': 10, 'Z': 10
        }
        for letter in word:
            sum += valueDict[letter]
        return sum

    def letterMupltiplier(self, valueCode):
        multDict = {
            'DL': 2,
            'TL': 3
        }
        return multDict.get(valueCode, 1)

    def wordMultiplier(self, valueCode):
        multDict = {
            'DW': 2,
            'TW': 3
        }
        return multDict.get(valueCode, 1)

    def extendRight(self, partialWord, node, row, col, firstAnchor, score):
        if row > 14 or col > 14:
            return
        if self.boardState[row][col].isEmpty():
            if node.endsWord and not firstAnchor:
                #found legal move
                foundMove = Move.Move(partialWord, row, col - 1, score)
                self.moveList.append(foundMove)
            for e in node.neighbors:
                workingScore = copy.deepcopy(score)
                if e in self.robotRack and self.crossCheckContains(e, row, col):
                    self.robotRack.remove(e)

                    #calculate score additions
                    letterScore = self.letterMupltiplier(self.boardState[row][col].special) * self.wordToScore(e)
                    sidePartScore = self.boardState[row][col].sideScore
                    wordMult = self.wordMultiplier(self.boardState[row][col].special)

                    workingScore.word += letterScore
                    #if a side word is made, add value for those tiles and for the added again
                    if sidePartScore > 0:
                        workingScore.sideParts += sidePartScore + self.wordToScore(e)
                    workingScore.wordMultiplier *= wordMult

                    self.extendRight(partialWord + e, node.neighbors[e], row, col + 1, False, copy.deepcopy(workingScore))
                    self.robotRack.append(e)
        else:
            if self.boardState[row][col].get() in node.neighbors:
                score.word += self.wordToScore(self.boardState[row][col].get())
                self.extendRight(partialWord + self.boardState[row][col].get(), node.neighbors[self.boardState[row][col].get()], row, col + 1, False, copy.deepcopy(score))

    def leftValue(self, partialWord, row, col, score):
        for i in range(len(partialWord)):
            square = self.boardState[row][col + i - len(partialWord)]
            score.word += self.letterMupltiplier(square.special) * self.wordToScore(partialWord[i])
            score.wordMultiplier *= self.wordMultiplier(square.special)

    def leftPart(self, partialWord, node, limit, row, col, score):
        # potential doesnt do anything
        self.leftValue(partialWord, row, col, score)
        self.extendRight(partialWord, node, row, col, True, score)
        if limit > 0:
            for e in node.neighbors:
                workingScore = copy.deepcopy(score)
                if e in self.robotRack:
                    self.robotRack.remove(e)

                    self.leftPart(partialWord + e, node.neighbors[e], limit - 1, row, col, Score.Score())
                    self.robotRack.append(e)
