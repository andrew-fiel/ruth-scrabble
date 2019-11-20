import Score


class Move:
    def __init__(self, word, row, col, score=Score.Score()):
        self.word = word
        self.row = row
        self.col = col
        self.isHorizontal = True
        self.score = score

    def __str__(self):
        returnstr = ""
        if self.isHorizontal:
            returnstr += "Horizontal word: "
        else:
            returnstr += "Vertical word: "
        returnstr += (self.word +
                      " of tile count: " +
                      str(self.score.tilesUsed) +
                      " ending at: " +
                      str(self.row) +
                      ", " +
                      str(self.col) +
                      " total score: " +
                      str(self.score.totalVal()))
        return returnstr

    def transpose(self):
        """Make a horizontal move vertical"""
        temp = self.row
        self.row = self.col
        self.col = temp
        self.isHorizontal = False
