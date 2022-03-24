import string
import tkinter as tk

from GuessBars import GuessBarEditable, GuessBar


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
