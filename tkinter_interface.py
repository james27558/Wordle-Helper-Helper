from ProgramInterface import ProgramInterface
from WordleHelperHelper import WordleHelperHelper

if __name__ == '__main__':
    interface = ProgramInterface()
    interface.bind("<Key>", interface.typeLetter)
    interface.bind("<space>", lambda x: print(interface.whh.filterWords()))
    interface.geometry("600x1000")
    interface.mainloop()
