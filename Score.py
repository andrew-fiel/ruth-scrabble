class Score:
    def __init__(self, word = 0, wordMultiplier = 1, sideParts = 0):
        self.word = word
        self.wordMultiplier = wordMultiplier
        self.sideParts = sideParts

    def totalVal(self):
        return self.word * self.wordMultiplier + self.sideParts
