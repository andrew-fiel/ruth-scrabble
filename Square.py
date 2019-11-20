class Square:

    def __init__(self, letter="", special="NA"):
        self.letter = letter
        self.anchor = False
        self.sideScore = 0

        # SPECIAL SQUARE VALUES
        # NA -- None / Regular Tile
        # DL -- Double Letter Score
        # TL -- Triple Letter Score
        # DW -- Double Word Score
        # TW -- Triple Word Score

        self.special = special

    def __str__(self):
        if self.letter == "":
            return " "
        else:
            return str(self.letter)

    def isEmpty(self):
        return self.letter == ""

    def isNotEmpty(self):
        return not self.isEmpty()

    def isAnchor(self):
        return self.anchor

    def setAnchor(self, isAnchor=True):
        self.anchor = isAnchor
        if self.isNotEmpty():
            self.anchor = False

    def add(self, newLetter):
        self.letter = newLetter
        self.anchor = False

    def remove(self):
        self.letter = ""

    def get(self):
        return self.letter
