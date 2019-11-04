import Board
import random
import Move

class Ruth:
    def __init__(self):
        self.horizontalBoard = Board.Board()
        self.verticalBoard = Board.Board()
        self.availableTiles = []

    def __str__(self):
        return str(self.horizontalBoard)

    def _addTile(self, letter, row, col):
        if len(letter) == 1:
            self.horizontalBoard.addTile(letter, row, col)
            #vertical words found with transpose of horizontal board state
            self.verticalBoard.addTile(letter, col, row)

    def reset(self):
        self.horizontalBoard.reset()
        self.verticalBoard.reset()

    def _generatePlayList(self):
        self.horizontalBoard.listPlays()
        self.verticalBoard.listPlays()
        for move in self.verticalBoard.moveList:
            move.transpose()
        playList = self.horizontalBoard.moveList + self.verticalBoard.moveList
        list.sort(playList, key=lambda play: play.score.totalVal(), reverse = True)
        return playList

    def _setRack(self, rack):
        self.horizontalBoard.robotRack = rack
        self.verticalBoard.robotRack = rack

    def _simulateGame(self):
        #first play is on center square
        self.horizontalBoard.boardState[7][7].setAnchor()
        self.verticalBoard.boardState[7][7].setAnchor()

        #make new order for tiles to be drawn in
        self.availableTiles = ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'D', 'D', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'F', 'F', 'G', 'G', 'G', 'H', 'H',
                                'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'J', 'K', 'L', 'L', 'L', 'L', 'M', 'M', 'N', 'N', 'N', 'N', 'N', 'N', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'P', 'P', 'Q',
                                'R', 'R', 'R', 'R', 'R', 'R', 'S', 'S', 'S', 'S', 'T', 'T', 'T', 'T', 'T', 'T', 'U', 'U', 'U', 'U', 'V', 'V', 'W', 'W', 'X', 'Y', 'Y', 'Z']

        random.shuffle(self.availableTiles)

        #play of the game placeholder with score 0
        potg = Move.Move("", 7, 7)

        compRack = []
        scorecount = 0
        while len(self.availableTiles) > 0:
            #draw until rack full
            while len(compRack) < 7 and len(self.availableTiles) > 0:
                compRack.append(self.availableTiles.pop())
            #print("rack = " + str(compRack))

            #if tiles in hand
            #if len(compRack) > 0:
            self._setRack(compRack)
            options = self._generatePlayList()
                #if there is a move to make

            if len(options) > 0:
                bestValueMove = options[0]
                self.makePlay(bestValueMove, compRack)
                scorecount += bestValueMove.score.totalVal()
                if bestValueMove.score.totalVal() > potg.score.totalVal():
                    potg = bestValueMove
            else:
                break
        self.reset()
        return potg

    def makePlay(self, move, rack):
        #starting row/col correction
        if move.isHorizontal:
            move.col -= len(move.word) - 1
        else:
            move.row -= len(move.word) - 1

        for l in range(len(move.word)):
            if self.horizontalBoard.boardState[move.row][move.col].isEmpty():
                self._addTile(move.word[l], move.row, move.col)
                rack.remove(move.word[l])
            if move.isHorizontal:
                move.col += 1
            else:
                move.row += 1
        if move.isHorizontal:
            move.col -= 1
        else:
            move.row -= 1

    def printMap(self, map):
        returnString = ""
        for row in map:
            for unit in row:
                returnString += '|' + str(unit)
            returnString += "|\n"
        print(returnString)



if __name__ == '__main__':
    game = Ruth()
    heatmap = [[0 for x in range(15)] for y in range(15)]
    for i in range(10):
        print("Starting game " + str(i))
        move = game._simulateGame()

        if move.isHorizontal:
            move.col -= len(move.word) - 1
        else:
            move.row -= len(move.word) - 1

        for l in range(len(move.word)):
            heatmap[move.row][move.col] += 1
            if move.isHorizontal:
                move.col += 1
            else:
                move.row += 1
        if move.isHorizontal:
            move.col -= 1
        else:
            move.row -= 1
        print("Game " + str(i) + " finished")
    game.printMap(heatmap)
