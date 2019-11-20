class Score:
    def __init__(self, word=0, wordMultiplier=1, sideParts=0, tilesUsed=0):
        self.word = word
        self.wordMultiplier = wordMultiplier
        self.sideParts = sideParts
        self.tilesUsed = tilesUsed

    def totalVal(self):
        """Returns total value of score"""
        # Test for Bingo
        if self.tilesUsed == 7:
            return self.word * self.wordMultiplier + self.sideParts + 50
        return self.word * self.wordMultiplier + self.sideParts

    def cheapishCopy(self):
        """Returns new score object copy"""
        return Score(self.word, self.wordMultiplier, self.sideParts, self.tilesUsed)
