import requests
from bs4 import BeautifulSoup



headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

URL = "https://gist.githubusercontent.com/cfreshman/a7b776506c73284511034e63af1017ee/raw/845966807347a7b857d53294525263408be967ce/wordle-nyt-answers-alphabetical.txt"

page = requests.get(URL, headers=headers)


soup = BeautifulSoup(page.content, "lxml")
res = soup.p.text
words = res.split("\n")
guesses = []

print(words)
