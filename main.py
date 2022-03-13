from enum import Enum

import requests
from bs4 import BeautifulSoup


class WordleHelperHelper:
    def __init__(self):
        self.guesses = []
        self.words = []
        self.bad_letters = []
        self.good_letters = []
        self.placed_letters = [[] * 5]

        self.search_mode = SearchMode.LINEAR

        self.fetchWords()

    def fetchWords(self):
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })

        URL = "https://gist.githubusercontent.com/cfreshman/a7b776506c73284511034e63af1017ee/raw/845966807347a7b857d53294525263408be967ce/wordle-nyt-answers-alphabetical.txt"
        page = requests.get(URL, headers=headers)

        soup = BeautifulSoup(page.content, "lxml")

        self.words = soup.p.text.split("\n")

    def setGuess(self, guess):
        self.guesses.append(guess)
        for c in guess:
            self.good_letters.append(c)

    def setBadLetter(self, bad_letter):
        self.bad_letters.append(bad_letter)

    def setGoodLetter(self, good_letter):
        self.good_letters.append(good_letter)

    def softReset(self):
        """
        Resets the fields such that the guesses are kept but the good, bad and placed letters are not
        :return:
        """

        self.good_letters = []
        self.bad_letters = []
        self.placed_letters = [[] * 5]


class SearchMode(Enum):
    LINEAR = 0

whh = WordleHelperHelper()