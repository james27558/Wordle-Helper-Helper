import string
import tkinter as tk
import ProgramInterface


class GuessBar(tk.Frame):
    """
    Wraps a frame to show and represent a guess on the board, editable or otherwise
    """

    def __init__(self, master, word=None, letter_boxes_colour_locked=False):
        super(GuessBar, self).__init__(master)
        self.program_interface: ProgramInterface.ProgramInterface = self.winfo_toplevel()

        # If the word is given then it must be 5 letters
        if word is not None:
            if len(word) != 5:
                raise ValueError("Word must be 5 letters")

            self.word = [tk.StringVar(value=x) for x in word]
        else:
            self.word = [tk.StringVar() for x in range(5)]

        # Initialise the letter boxes, if the letter_boxes_colour_locked is True then the letter boxes colours will be
        # locked to stop the user marking them as good/placed. Used for the editable guess bar
        self.letter_boxes = [LetterBox(self, tv=self.word[x], position=x, colour_locked=letter_boxes_colour_locked) for
                             x in range(5)]

        for i, v in enumerate(self.letter_boxes):
            self.letter_boxes[i].grid(row=0, column=i)

    def getFullWord(self):
        """
        Get all the letters in the letter boxes joined into one string, the contents of blank boxes will not appear

        :return: All letters as string
        """
        return "".join([x.get() for x in self.word])

    def getLetterBoxes(self):
        return self.letter_boxes

    def addDuplicateLettersToHelper(self):
        """
        If any letters in the guess appear multiple times, either good or placed, then try to add it to the duplicate
        letters list

        :return:
        """
        seen_good_or_placed_letters = []

        for letter_box in self.letter_boxes:
            letter = letter_box.getLetter()

            # If the letter is coloured
            if letter_box.placed_letter or letter_box.good_letter:
                # If the letter hasn't been 'seen' yet in the loop through the letters then mark it as 'seen'
                if letter not in seen_good_or_placed_letters:
                    seen_good_or_placed_letters.append(letter)
                else:
                    # Otherwise, it has been 'seen' and this letter is a duplicate in this guess, so it should be added
                    # to the Helper as a duplicate letter
                    self.program_interface.whh.setDuplicateLetter(letter)


class GuessBarEditable(GuessBar):
    """
    Wraps GuessBar to allow it to be edited, provides methods for setting and unsetting characters, has a limit of 5
    letters
    """

    def __init__(self, master):
        # Init the GuessBar superclass and tell it to lock the colours (good/placed) of letter boxes
        super().__init__(master, letter_boxes_colour_locked=True)

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
    def __init__(self, master: GuessBar, tv, position, colour_locked = False):
        """
        :param master:
        :param tv:
        :param position: 0 indexed position
        """
        super(LetterBox, self).__init__(master, bg="black", fg="white", padx=5, pady=5, width=1, textvariable=tv)
        self.my_master = master
        self.position = position
        self.colour_locked = colour_locked
        self.tv: tk.StringVar = tv
        self.bind("<Button-1>", self.parseLeftClick)
        self.bind("<Button-3>", self.parseRightClick)

        self.good_letter = False
        self.placed_letter = False

        self.program_interface: ProgramInterface.ProgramInterface = self.winfo_toplevel()

    def parseLeftClick(self, click):
        """
        Sets placed letter

        :param click:
        :return:
        """
        if self.good_letter or self.colour_locked: return

        if not self.placed_letter:
            self.program_interface.whh.setPlacedLetter(self.tv.get(), self.position)
            self.__placedLetterColourScheme()
            self.placed_letter = True
            self.my_master.addDuplicateLettersToHelper()

        else:
            self.program_interface.whh.deletePlacedLetter(self.tv.get(), self.position)
            self.__defaultColourScheme()
            self.placed_letter = False

    def parseRightClick(self, click):
        """
        Sets good letter

        :param click:
        :return:
        """
        if self.placed_letter or self.colour_locked: return

        if not self.good_letter:
            self.program_interface.whh.setGoodLetter(self.tv.get(), self.position)
            self.__goodLetterColourScheme()
            self.good_letter = True
            self.my_master.addDuplicateLettersToHelper()

        else:
            self.program_interface.whh.deleteGoodLetter(self.tv.get(), self.position)
            self.__defaultColourScheme()
            self.good_letter = False

    def softResetColourScheme(self):
        self.good_letter = False
        self.placed_letter = False
        self.__defaultColourScheme()

    def getLetter(self):
        """
        Gets the letter in this letter box

        :return: Letter in the letter box
        """

        return self.tv.get()

    def __defaultColourScheme(self):
        self.configure(bg="black", fg="white")

    def __placedLetterColourScheme(self):
        self.configure(bg="green")

    def __goodLetterColourScheme(self):
        self.configure(bg="yellow", fg="black")