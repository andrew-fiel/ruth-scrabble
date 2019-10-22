class Square:

    def __init__(self, letter = ""):
        self.letter = letter

    def __str__(self):
        if self.letter == "":
            return " "
        else:
            return str(self.letter)

    def isEmpty(self):
        return self.letter == ""

    def isNotEmpty(self):
        return not self.isEmpty()

    def add(self, newLetter):
        self.letter = newLetter

    def remove(self):
        self.letter = ""

    def get(self):
        return self.letter
