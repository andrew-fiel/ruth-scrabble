import Move
import Square
import pickle
import Score


class Board:
    def __init__(self):
        self.boardState = [[Square.Square() for x in range(15)] for y in range(15)]
        # Place x of pink Double Word score
        for row in range(15):
            for col in range(15):
                if row == col:
                    self.boardState[row][col].special = "DW"
                if 14 - col == row:
                    self.boardState[row][col].special = "DW"
        # Place the rest manually because weird patterns
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

        # 67108863 is bit vector of every letter
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
        """Adds tile and updates relevant adjacency"""
        if len(letter) == 1 and self.boardState[row][col].isEmpty():
            self.boardState[row][col].add(letter)
        else:
            raise Exception("Tile must be of length 1 and position must be empty")

        if row + 1 < 15:
            self._updateAdjacencyOfTile(row + 1, col)
        if row - 1 >= 0:
            self._updateAdjacencyOfTile(row - 1, col)

        if row < 14 and self.boardState[row + 1][col].isEmpty():
            self.boardState[row + 1][col].setAnchor()
        if row > 0 and self.boardState[row - 1][col].isEmpty():
            self.boardState[row - 1][col].setAnchor()
        if col < 14 and self.boardState[row][col + 1].isEmpty():
            self.boardState[row][col + 1].setAnchor()
        if col > 0 and self.boardState[row][col - 1].isEmpty():
            self.boardState[row][col - 1].setAnchor()
        changeRow = row

        # if word bellow, follow it and update the adj of the closest free space
        if changeRow + 1 < 15 and self.boardState[changeRow + 1][col].isNotEmpty():
            while changeRow < 13:
                changeRow += 1
                if self.boardState[changeRow + 1][col].isEmpty():
                    self._updateAdjacencyOfTile(changeRow + 1, col)
                    break
        # if word above, follow it and update the adj of the closest free space
        changeRow = row
        if changeRow - 1 >= 0 and self.boardState[changeRow - 1][col].isNotEmpty():
            while changeRow > 1:
                changeRow -= 1
                if self.boardState[changeRow - 1][col].isEmpty():
                    self._updateAdjacencyOfTile(changeRow - 1, col)
                    break

    def _updateAdjacencyOfTile(self, row, col):
        """Updates sidescore and adjacency of tile"""
        options = []
        # if tile immediately above and below filled
        if (row > 0 and self.boardState[row - 1][col].isNotEmpty() and
                row < 14 and self.boardState[row + 1][col].isNotEmpty()):
            wordStart = self._findWordStart(row - 1, col, 1)
            wordEnd = self._findWordStart(row + 1, col, 3)
            hasBothOptions = self.dictionary.lookupBoth(wordStart, wordEnd)
            # set values used for scoring later
            self.boardState[row][col].sideScore = self._wordToScore(wordStart)
            self.boardState[row][col].sideScore += self._wordToScore(wordEnd)
            if hasBothOptions[0]:
                options += hasBothOptions[1]

        else:
            # just tile above
            if row > 0 and row < 15 and self.boardState[row - 1][col].isNotEmpty():
                wordStart = self._findWordStart(row - 1, col, 1)
                hasUps = self.dictionary.lookupEndOptions(wordStart)
                self.boardState[row][col].sideScore = self._wordToScore(wordStart)
                if hasUps[0]:
                    options += hasUps[1]
            # just tile below
            if row < 14 and row >= 0 and self.boardState[row + 1][col].isNotEmpty():
                wordEnd = self._findWordStart(row + 1, col, 3)
                hasDowns = self.dictionary.lookupStartOptions(wordEnd)
                self.boardState[row][col].sideScore = self._wordToScore(wordEnd)
                if hasDowns[0]:
                    options += hasDowns[1]
        value = 0
        for option in options:
            tempVal = ord(option) - ord('A')
            if tempVal >= 0 and tempVal < 26:
                num = 1 << tempVal
            value = value | num
        self.adjacentBitVector[row][col] = value

    def _findWordStart(self, row, col, direction):
        """ Direction should be 1-4. Assumes row, col given is legitimate start to word"""
        wordStart = ""
        wordStart += self.boardState[row][col].get()
        if direction == 1:
            # up
            while row > 0 and self.boardState[row - 1][col].isNotEmpty():
                wordStart = self.boardState[row - 1][col].get() + wordStart
                row -= 1
        elif direction == 2:
            # right
            while col < 14 and self.boardState[row][col + 1].isNotEmpty():
                wordStart += self.boardState[row][col + 1].get()
                col += 1
        elif direction == 3:
            # down
            while row < 14 and self.boardState[row + 1][col].isNotEmpty():
                wordStart += self.boardState[row + 1][col].get()
                row += 1
        elif direction == 4:
            # left
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
                    # case anchor immediately right of extant letter
                    if (colIndex > 0 and
                            self.boardState[rowIndex][colIndex - 1].isNotEmpty()):
                        iterNode = self.dictionary.root
                        # 4 means look left
                        wordStart = self._findWordStart(rowIndex, colIndex, 4)
                        for x in range(colIndex - len(wordStart), colIndex):
                            currentSquare = self.boardState[rowIndex][x]
                            if currentSquare.get() not in iterNode.neighbors:
                                raise Exception("Illegal word on board")
                            iterNode = iterNode.neighbors[currentSquare.get()]
                            adding = self._wordToScore(currentSquare.get())
                            score.word += adding
                        self._extendRight(wordStart, iterNode,
                                          rowIndex, colIndex, True, score)
                    else:
                        self._leftPart("", self.dictionary.root,
                                       k, rowIndex, colIndex, score)
                    k = 0

                else:
                    k += 1

    def _crossCheckContains(self, letter, row, col):
        value = self.adjacentBitVector[row][col]
        shiftAmount = ord(letter) - ord('A')
        if ((1 << shiftAmount) & value) != 0:
            # in bit vector
            return True
        return False

    def _wordToScore(self, word):
        """Calculates value of word from tiles alone"""
        sum = 0
        valueDict = {
            '?': 0,
            'E': 1, 'A': 1, 'I': 1, 'O': 1, 'N': 1,
            'R': 1, 'T': 1, 'L': 1, 'S': 1, 'U': 1,
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

    def _letterMultiplier(self, valueCode):
        """Converts special letter tile to value"""
        multDict = {
            'DL': 2,
            'TL': 3
        }
        return multDict.get(valueCode, 1)

    def _wordMultiplier(self, valueCode):
        """Converts special word tile to value"""
        multDict = {
            'DW': 2,
            'TW': 3
        }
        return multDict.get(valueCode, 1)

    def _extendRight(self, partialWord, node, row, col, firstAnchor, score):
        """Place right portion of word"""
        if row > 14:
            return
        if col == 15:
            if node.endsWord and not firstAnchor:
                # found legal move
                foundMove = Move.Move(partialWord, row, col - 1, score)
                self.moveList.append(foundMove)
            return
        if self.boardState[row][col].isEmpty():
            if node.endsWord and not firstAnchor:
                # found legal move
                foundMove = Move.Move(partialWord, row, col - 1, score)
                self.moveList.append(foundMove)
            for e in node.neighbors:
                workingScore = score.cheapishCopy()
                if e in self.robotRack and self._crossCheckContains(e, row, col):
                    self.robotRack.remove(e)

                    # calculate score additions
                    letterS = (self._letterMultiplier(self.boardState[row][col].special) *
                               self._wordToScore(e))
                    sidePartScore = self.boardState[row][col].sideScore
                    wordMult = self._wordMultiplier(self.boardState[row][col].special)

                    workingScore.word += letterS
                    # if a side word is made, add value for the whole word
                    if sidePartScore > 0:
                        workingScore.sideParts += sidePartScore + self._wordToScore(e)
                    workingScore.wordMultiplier *= wordMult

                    workingScore.tilesUsed += 1

                    self._extendRight(partialWord + e,
                                      node.neighbors[e],
                                      row,
                                      col + 1,
                                      False,
                                      workingScore.cheapishCopy())
                    self.robotRack.append(e)
        else:
            if self.boardState[row][col].get() in node.neighbors:
                score.word += self._wordToScore(self.boardState[row][col].get())
                self._extendRight(partialWord + self.boardState[row][col].get(),
                                  node.neighbors[self.boardState[row][col].get()],
                                  row,
                                  col + 1,
                                  False,
                                  score.cheapishCopy())

    def _leftValue(self, partialWord, row, col, score):
        """Calculate value of left part of word after it has been placed"""
        for i in range(len(partialWord)):
            square = self.boardState[row][col + i - len(partialWord)]
            score.word += (self._letterMultiplier(square.special) *
                           self._wordToScore(partialWord[i]))
            score.wordMultiplier *= self._wordMultiplier(square.special)
        score.tilesUsed = len(partialWord)

    def _leftPart(self, partialWord, node, limit, row, col, score):
        """Create options for left part"""
        self._leftValue(partialWord, row, col, score)
        self._extendRight(partialWord, node, row, col, True, score)
        if limit > 0:
            for e in node.neighbors:
                if e in self.robotRack:
                    self.robotRack.remove(e)

                    self._leftPart(partialWord + e,
                                   node.neighbors[e],
                                   limit - 1,
                                   row,
                                   col,
                                   Score.Score())
                    self.robotRack.append(e)
