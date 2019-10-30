class Move:
    def __init__(self, word, row, col, score):
        self.word = word
        self.row = row
        self.col = col
        self.isHorizontal = True
        self.score = score

    def __str__(self):
        if self.isHorizontal:
            return "Horizontal word: " + self.word + " ending at: " + str(self.row) + ", " + str(self.col) + " word score: " + str(self.score.word) + " side: " + str(self.score.sideParts) + " and mult: " + str(self.score.wordMultiplier)
        else:
            return "Vertical word: " + self.word + " ending at: " + str(self.row) + ", " + str(self.col) + " word score: " + str(self.score.word) + " side: " + str(self.score.sideParts) + " and mult: " + str(self.score.wordMultiplier)
    def transpose(self):
        temp = self.row
        self.row = self.col
        self.col = temp
        self.isHorizontal = False
