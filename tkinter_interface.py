import string
import tkinter as tk
from WordleHelperHelper import WordleHelperHelper


class ProgramInterface(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # self.whh = WordleHelperHelper()

        # (Pycharm IDE Annotation)
        # noinspection PyTypeChecker
        self.current_guess_bar: GuessBarEditable = None
        self.next_guess_bar_row_index = 0

        self.all_guess_bars = []

        self.initialiseWidgets()

    def typeLetter(self, key):
        # Delete a letter from the guess if the user has typed a backspace
        typed_key = key.keysym

        if typed_key == "BackSpace":
            self.current_guess_bar.backspace()

        # Otherwise, if it is a letter, add it if it won't put the guess over 5 letters
        elif typed_key.lower() in string.ascii_lowercase:
            self.current_guess_bar.typeLetter(typed_key.lower())

        elif typed_key == "Return":
            full_word = self.current_guess_bar.getFullWord()

            if len(full_word) == 5:
                self.addNewGuessToBoard(full_word)

    def initialiseWidgets(self):
        """
        Initialise and place the editable guess box on the window
        :return:
        """
        self.current_guess_bar = GuessBarEditable(self)

        self.current_guess_bar.grid(column=0, row=self.next_guess_bar_row_index + 1)

    def addNewGuessToBoard(self, guess: string):
        """
        Adds a new static guess to the board and moves down the editable guess box
        :param guess: Word to add to the board
        :return:
        """

        # Create the new guess
        new_bar = GuessBar(self, guess)
        new_bar.grid(row=self.next_guess_bar_row_index, column=0)

        # Add it to the list of bars
        self.all_guess_bars.append(new_bar)

        # Move the index further down the pane
        self.next_guess_bar_row_index += 1

        # Move the editable guess box down
        self.current_guess_bar.grid(column=0, row=self.next_guess_bar_row_index + 1)

        # Reset the word in the bar
        self.current_guess_bar.reset()


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

        self.letter_boxes = [LetterBox(self, tv=self.word[x]) for x in range(5)]

        for i, v in enumerate(self.letter_boxes):
            self.letter_boxes[i].grid(row=0, column=i)

    def getFullWord(self):
        return "".join([x.get() for x in self.word])


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


class LetterBox(tk.Label):
    def __init__(self, master, tv):
        super(LetterBox, self).__init__(master, bg="black", fg="white", textvariable=tv)


if __name__ == '__main__':
    interface = ProgramInterface()
    interface.bind("<Key>", interface.typeLetter)
    interface.geometry("600x1000")
    interface.mainloop()
