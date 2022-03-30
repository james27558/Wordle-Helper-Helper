from ProgramInterface import ProgramInterface
from WordleHelperHelper import WordleHelperHelper

if __name__ == '__main__':
    interface = ProgramInterface()
    interface.bind("<Key>", interface.typeLetter)
    interface.bind("<space>", lambda x: print(len(interface.whh.filterWords()), interface.whh.filterWords()))
    interface.geometry("300x500")
    interface.mainloop()
