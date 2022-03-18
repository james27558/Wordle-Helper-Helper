import unittest
import unittest.mock as mock
from WordleHelperHelper import WordleHelperHelper


class WordleHelperHelperTestCase(unittest.TestCase):
    def setUp(self):
        self.whh = WordleHelperHelper()
        self.whh.fetchAndStoreWords()

    def tearDown(self):
        self.whh.hardReset()

    def test_fetchAndStoreWords_populatesArray(self):
        self.assertTrue(len(self.whh.all_answers) > 0)

    def test_badLetters_eliminateLetterFromSolutions(self):
        excluded_letter = "a"

        self.whh.setBadLetter(excluded_letter)
        words = self.whh.filterWords()

        for i in words:
            self.assertTrue(excluded_letter not in i)

    def test_badLetters_eliminateLettersFromSolutions(self):
        excluded_letters = ["a", "b"]

        for i in excluded_letters:
            self.whh.setBadLetter(i)

        words = self.whh.filterWords()

        for i in words:
            for j in excluded_letters:
                self.assertTrue(j not in i)

    def test_settingConflictingPlacedBadLetters_throwsValueError(self):
        self.whh.setPlacedLetter("a", 1)
        self.assertRaises(ValueError, self.whh.setBadLetter, "a")

    def test_settingConflictingBadPlacedLetters_OverwritesBadLetter(self):
        self.whh.setBadLetter("a")
        self.whh.setPlacedLetter("a", 1)

        self.assertListEqual(self.whh.bad_letters, [])
        self.assertTrue("a" in self.whh.getPlacedLettersList())

    def test_GoodLetterPositions_EliminatesWordsWithThatLetterInThatPosition(self):
        self.whh.setGoodLetter("a", 1)

        for word in self.whh.filterWords():
            self.assertTrue("a" in word and word[1] != "a")


if __name__ == '__main__':
    unittest.main()
