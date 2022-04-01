import string
import tkinter as tk

from GuessBars import GuessBarEditable, GuessBar
from WordleHelperHelper import WordleHelperHelper


class ProgramInterface(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.whh = WordleHelperHelper()
        self.whh.fetchAndStoreWords()

        # (Pycharm IDE Annotation)
        # noinspection PyTypeChecker
        self.current_guess_bar: GuessBarEditable = None
        self.next_guess_bar_row_index = 0

        self.all_guess_bars: list[GuessBar] = []

        self.hard_reset_button: tk.Button = None

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

    def addGoodLetter(self, letter, position):
        f"""
        Wrapper for setGoodLetter in @{WordleHelperHelper}
        :param letter:
        :param position:
        :return:
        """

        self.whh.setGoodLetter(letter, position)

    def addPlacedLetter(self, letter, position):
        f"""
        Wrapper for setPlacedLetter in @{WordleHelperHelper}
        :param letter:
        :param position:
        :return:
        """

        self.whh.setPlacedLetter(letter, position)

    def initialiseWidgets(self):
        """
        Initialise and place the editable guess box on the window
        :return:
        """
        self.current_guess_bar = GuessBarEditable(self)
        self.current_guess_bar.grid(column=0, row=0, columnspan=5)

        self.hard_reset_button = tk.Button(self, text="Reset All Guesses", command=self.hardReset)
        self.hard_reset_button.grid(row=0, column=7, columnspan=2)

        self.soft_reset_button = tk.Button(self, text="Soft Reset Board", command=self.softReset)
        self.soft_reset_button.grid(row=1, column=7, columnspan=2)

    def hardReset(self):
        f"""
        Hard resets the @{WordleHelperHelper} instance and deletes the guesses on the board
        :return: 
        """
        self.whh.hardReset()

        # Reset variables
        self.next_guess_bar_row_index = 0

        # Move up the current guess bar
        self.current_guess_bar.grid(column=0, row=0, columnspan=5)

        # Destroy all permanent guess bars
        for guess in self.all_guess_bars:
            guess.destroy()

        # Clear the list of bars
        self.all_guess_bars.clear()

    def softReset(self):
        f"""
        Soft resets the @{WordleHelperHelper} instance and deletes the good/placed letters on the board
        :return: 
        """
        self.whh.softReset()

        for bar in self.all_guess_bars:
            for letter_box in bar.letter_boxes:
                letter_box.softResetColourScheme()



    def addNewGuessToBoard(self, guess: string):
        """
        Adds a new static guess to the board and moves down the editable guess box, adding the letters in the guess to
        the bad letters list. The user will mark the letters on the board good or placed, removing them from the bad
        letters list

        :param guess: Word to add to the board
        :return:
        """

        # Extract bad letters when adding guess
        self.whh.extractBadLetters(guess)

        # Create the new guess
        new_bar = GuessBar(self, guess)
        new_bar.grid(row=self.next_guess_bar_row_index, column=0, columnspan=5)

        # Add it to the list of bars
        self.all_guess_bars.append(new_bar)

        # Move the index further down the pane
        self.next_guess_bar_row_index += 1

        # Move the editable guess box down
        self.current_guess_bar.grid(column=0, row=self.next_guess_bar_row_index + 1, columnspan=5)

        # Reset the word in the bar
        self.current_guess_bar.reset()
