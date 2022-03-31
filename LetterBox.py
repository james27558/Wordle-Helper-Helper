import tkinter as tk

import ProgramInterface


class LetterBox(tk.Label):
    def __init__(self, master, tv, position):
        """
        :param master:
        :param tv:
        :param position: 0 indexed position
        """
        super(LetterBox, self).__init__(master, bg="black", fg="white", padx=5, pady=5, width=1, textvariable=tv)
        self.position = position
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
        if self.good_letter: return

        if not self.placed_letter:
            self.program_interface.whh.setPlacedLetter(self.tv.get(), self.position)
            self.__placedLetterColourScheme()
            self.placed_letter = True

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
        if self.placed_letter: return

        if not self.good_letter:
            self.program_interface.whh.setGoodLetter(self.tv.get(), self.position)
            self.__goodLetterColourScheme()
            self.good_letter = True

        else:
            self.program_interface.whh.deleteGoodLetter(self.tv.get(), self.position)
            self.__defaultColourScheme()
            self.good_letter = False

    def softResetColourScheme(self):
        self.good_letter = False
        self.placed_letter = False
        self.__defaultColourScheme()

    def __defaultColourScheme(self):
        self.configure(bg="black", fg="white")

    def __placedLetterColourScheme(self):
        self.configure(bg="green")

    def __goodLetterColourScheme(self):
        self.configure(bg="yellow", fg="black")
