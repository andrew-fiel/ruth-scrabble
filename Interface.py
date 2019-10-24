import Board

class Ruth:
    def __init__(self):
        self.horizontalBoard = Board.Board()
        self.verticalBoard = Board.Board()

    def __str__(self):
        return str(self.horizontalBoard)

    def _addTile(self, letter, row, col):
        if len(letter) == 1:
            self.horizontalBoard.addTile(letter, row, col)
            #vertical words found with transpose of horizontal board state
            self.verticalBoard.addTile(letter, col, row)

    def _generatePlayList(self):
        self.horizontalBoard.listPlays()
        self.verticalBoard.listPlays()
        for move in self.verticalBoard.moveList:
            move.transpose()
        playList = self.horizontalBoard.moveList + self.verticalBoard.moveList
        return playList

    def _setRack(self, rack):
        self.horizontalBoard.robotRack = rack
        self.verticalBoard.robotRack = rack

if __name__ == '__main__':
    game = Ruth()
    game._addTile('C', 5, 3)
    game._addTile('A', 5, 4)
    print(game)
    game._setRack(['B', 'T', 'D'])
    for move in game._generatePlayList():
        print(str(move))
