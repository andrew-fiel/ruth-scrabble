class Move:
    def __init__(self, word, row, col, score):
        self.word = word
        self.row = row
        self.col = col
        self.isHorizontal = True
        self.score = score

    def __str__(self):
        if self.isHorizontal:
            return "Horizontal word: " + self.word + " ending at: " + str(self.row) + ", " + str(self.col) + " total score: " + str(self.score.totalVal())
        else:
            return "Vertical word: " + self.word + " ending at: " + str(self.row) + ", " + str(self.col) + " total score: " + str(self.score.totalVal())
    def transpose(self):
        temp = self.row
        self.row = self.col
        self.col = temp
        self.isHorizontal = False
