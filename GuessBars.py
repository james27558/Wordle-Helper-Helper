import tkinter as tk

from LetterBox import LetterBox


class GuessBar(tk.Frame):
    """
    Wraps a frame to show and represent a guess on the board, editable or otherwise
    """

    def __init__(self, master, word=None):
        super(GuessBar, self).__init__(master)

        # If the word is given then it must be 5 letters
        if word is not None:
            if len(word) != 5:
                raise ValueError("Word must be 5 letters")

            self.word = [tk.StringVar(value=x) for x in word]
        else:
            self.word = [tk.StringVar() for x in range(5)]

        self.letter_boxes = [LetterBox(self, tv=self.word[x], position=x) for x in range(5)]

        for i, v in enumerate(self.letter_boxes):
            self.letter_boxes[i].grid(row=0, column=i)

    def getFullWord(self):
        return "".join([x.get() for x in self.word])

    def getLetterBoxes(self):
        return self.letter_boxes


class GuessBarEditable(GuessBar):
    """
    Wraps GuessBar to allow it to be edited, provides methods for setting and unsetting characters, has a limit of 5
    letters
    """

    def __init__(self, master):
        super().__init__(master)

        # Index of the next letter that is empty, 6 if none
        self.next_empty_letter_index = 0

    def setLetter(self, letter, index):
        """
        Sets a letter at the index given and increases the next available index by 1
        :param letter:
        :param index:
        :return:
        """
        self.word[index].set(letter)
        self.next_empty_letter_index += 1

    def setLetterAtNextAvailableIndex(self, letter):
        """
        Sets a letter in the next available position, if all 5 positions are filled, does nothing.
        :param letter:
        :return:
        """
        if self.next_empty_letter_index != 5:
            self.setLetter(letter, self.next_empty_letter_index)

    def unsetIndex(self, index):
        """
        Unsets a letter at the index given and reduces the next available index by 1
        :param index:
        :return:
        """
        self.word[index].set("")
        self.next_empty_letter_index -= 1

    def unsetLetterBeforeNextAvailableIndex(self):
        """
        Unsets a letter at next available position - 1, if there are no letters to unset (available index i=0),
        does nothing.
        :return:
        """
        if self.next_empty_letter_index != 0:
            self.unsetIndex(self.next_empty_letter_index - 1)

    def backspace(self):
        """
        Alias for unsetLetterBeforeNextAvailableIndex()
        :return:
        """
        self.unsetLetterBeforeNextAvailableIndex()

    def typeLetter(self, letter):
        """
        Alias for setLetterAtNextAvailableIndex(letter)
        :param letter:
        :return:
        """
        self.setLetterAtNextAvailableIndex(letter)

    def reset(self):
        """
        Unsets all letters
        :return:
        """
        while self.next_empty_letter_index != 0:
            self.unsetLetterBeforeNextAvailableIndex()
