import tkinter as tk


class LetterBox(tk.Label):
    def __init__(self, master, tv):
        super(LetterBox, self).__init__(master, bg="black", fg="white", textvariable=tv)
