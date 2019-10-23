class Move:
    def __init__(self, word, row, col):
        self.word = word
        self.row = row
        self.col = col

    def __str__(self):
        return "Word: " + self.word + " ending at: " + str(self.row) + ", " + str(self.col)
