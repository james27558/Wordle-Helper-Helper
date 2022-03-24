from ProgramInterface import ProgramInterface
from WordleHelperHelper import WordleHelperHelper

if __name__ == '__main__':
    interface = ProgramInterface()
    interface.bind("<Key>", interface.typeLetter)
    interface.geometry("600x1000")
    interface.mainloop()
