import string
from enum import Enum
from typing import List

import requests
from bs4 import BeautifulSoup


class WordleHelperHelper:
    def __init__(self):
        """
        List of guessed words
        """
        self.guesses = []

        """
        List of all possible answers
        """
        self.all_answers = []

        """
        List of characters that are the bad letters for the current word
        """
        self.bad_letters = []

        """
        2D list of pairs of characters and 0 indexed positions in the word
        """
        self.good_letters = []

        """
        List of 5 None or characters, that represent the placed letters in the current word
        """
        self.placed_letters = [None, None, None, None, None]

        self.search_mode = SearchMode.LINEAR

        self.fetchAndStoreWords()

        self.mainloop()

    def mainloop(self):
        while True:
            print("1. Add guess")
            print("2. Print Words")
            print("4. Soft Reset")
            print("5. Hard Reset")

            choice = input("What would you like to do: ")

            if choice == "1":
                input_string = input("Guess {word} {placed letter indexes , seperated} {good letter indexes , "
                                     "seperated}: ")

                guess_info = input_string.split(" ")
                guess = guess_info[0]
                placed_letter_indexes = guess_info[1].split(",")
                placed_letter_indexes = [] if placed_letter_indexes == ["None"] else placed_letter_indexes
                placed_letter_indexes = list(map(lambda x: int(x) - 1, placed_letter_indexes))

                good_letter_indexes = guess_info[2].split(",")
                good_letter_indexes = [] if good_letter_indexes == ["None"] else good_letter_indexes
                good_letter_indexes = list(map(lambda x: int(x) - 1, good_letter_indexes))

                self.parseGuessWithPlacedPlusGoodLetters(guess, placed_letter_indexes, good_letter_indexes)

            elif choice == "2":
                print(self.filterWords())

            elif choice == "4":
                self.softReset()

            elif choice == "5":
                self.hardReset()

    def fetchAndStoreWords(self):
        """
        Fetches the list of words from the github repository and stores them in the class
        :return:
        """
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })

        URL = "https://gist.githubusercontent.com/cfreshman/a7b776506c73284511034e63af1017ee/raw/845966807347a7b857d53294525263408be967ce/wordle-nyt-answers-alphabetical.txt"
        page = requests.get(URL, headers=headers)

        soup = BeautifulSoup(page.content, "lxml")

        self.all_answers = soup.p.text.split("\n")

    def setGuess(self, guess: string):
        self.guesses.append(guess)

    def extractBadLetters(self, guess: string):
        """
        Takes a guess and extracts the letters that aren't already in the good/placed letters list and adds them to
        the bad letters list
        :param guess: Guess to extract bad letters from
        :return:
        """

        for c in guess:
            if c not in self.getPlacedLettersList() and c not in self.getGoodLetterList():
                self.bad_letters.append(c)

    def getGoodLetterList(self):
        """
        Returns a list of characters in good letters
        :return:
        """
        return [x[0] for x in self.good_letters]

    def getPlacedLettersList(self):
        return self.placed_letters

    def parseGuessWithPlacedPlusGoodLetters(self, guess: string, placed_indexes: List[int], good_indexes: List[int]):
        """

        :param guess:
        :param placed_indexes:
        :param good_indexes:
        :return:
        """

        for good_index in good_indexes:
            self.setGoodLetter(guess[good_index], good_index)

        for placed_index in placed_indexes:
            self.setPlacedLetter(guess[placed_index], placed_index)

        self.extractBadLetters(guess)
        self.setGuess(guess)

    def setBadLetter(self, bad_letter: string):
        self.bad_letters.append(bad_letter)

    def setGoodLetter(self, good_letter: string):
        self.good_letters.append((good_letter, -1))

    def setGoodLetter(self, good_letter: string, position: int):
        self.good_letters.append((good_letter, position))

    def setPlacedLetter(self, letter: string, position: int):
        """
        Sets a placed letter in the current word
        :param letter: Placed letter
        :param position: Position (0 indexed)
        :return:
        """

        self.placed_letters[position] = letter

    def softReset(self):
        """
        Resets the fields such that the guesses are kept but the good, bad and placed letters are not. Useful for
        wordle type games with >1 word, where you'd want to keep the guesses, as they're persistent between words,
        whereas good, bad and placed letters aren't
        :return:
        """

        self.good_letters = []
        self.bad_letters = []
        self.placed_letters = [None, None, None, None, None]

    def hardReset(self):
        """
        Resets all fields used
        :return:
        """
        self.softReset()
        self.guesses = []

    def filterWords(self):
        valid_words = []
        for word in self.all_answers:
            valid = True

            # Loop through the placed letters, if it isn't present in the correct position then mark the work as invalid
            for index, letter in enumerate(self.getPlacedLettersList()):
                if letter is not None:
                    if word[index] != letter:
                        valid = False
                        break

            # If the word has been marked as invalid then skip checking other attributes
            if not valid:
                continue  # Outer loop

            # TODO: Account for good letter positions

            for good_letter_info in self.good_letters:
                letter = good_letter_info[0]
                position = good_letter_info[1]

                if letter not in word:
                    valid = False
                    break

            # If the word has been marked as invalid then skip checking other attributes
            if not valid:
                continue  # Outer loop

            for bad_letter in self.bad_letters:
                if bad_letter in word:
                    valid = False
                    break

            # If the word has been marked as invalid then don't continue to appending the word
            if not valid:
                continue  # Outer loop

            valid_words.append(word)

        return valid_words


class SearchMode(Enum):
    LINEAR = 0


whh = WordleHelperHelper()
