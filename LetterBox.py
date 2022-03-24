import tkinter as tk

import ProgramInterface


class LetterBox(tk.Label):
    def __init__(self, master, tv, position):
        """
        :param master:
        :param tv:
        :param position: 0 indexed position
        """
        super(LetterBox, self).__init__(master, bg="black", fg="white", textvariable=tv)
        self.position = position
        self.tv: tk.StringVar = tv
        self.bind("<Button-1>", self.parseLeftClick)
        self.bind("<Button-3>", self.parseRightClick)

        self.good_letter = False
        self.placed_letter = False

        self.program_interface: ProgramInterface.ProgramInterface = self.winfo_toplevel()

    def parseLeftClick(self, click):
        if not self.placed_letter:
            self.program_interface.whh.setPlacedLetter(self.tv.get(), self.position)
            self.placedLetterColourScheme()
            self.placed_letter = True

        else:
            self.defaultColourScheme()
            self.placed_letter = False

    def parseRightClick(self, click):
        if not self.good_letter:
            self.program_interface.whh.setGoodLetter(self.tv.get(), self.position)
            self.goodLetterColourScheme()
            self.good_letter = True

        else:
            self.defaultColourScheme()
            self.good_letter = False

    def defaultColourScheme(self):
        self.configure(bg="black", fg="white")

    def placedLetterColourScheme(self):
        self.configure(bg="green")

    def goodLetterColourScheme(self):
        self.configure(bg="yellow", fg="black")
