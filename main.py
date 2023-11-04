import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
import re
from time import sleep

def ascii_art():
    print("live cricket score")

def get_current_matches():
    page = requests.get('http://static.cricinfo.com/rss/livescores.xml')
    soup = BeautifulSoup(page.text, 'lxml')
    matches = soup.find_all('description')
    live_matches = [s.get_text() for s in matches if '*' in s.get_text()]
    return live_matches

def fetch_score(matchNum):
    # Function to return the live score of the match specified
    page = requests.get('http://static.cricinfo.com/rss/livescores.xml')
    soup = BeautifulSoup(page.text, 'lxml')
    matches = soup.find_all('description')
    live_matches = [s.get_text() for s in matches if '*' in s.get_text()]
    return live_matches[matchNum]

def notify(score):
    # Function for Windows toast desktop notification
    toaster = ToastNotifier()
    toaster.show_toast(score, "Let's Play Cricket...", duration=30)

# The Main Function
if __name__ == "__main__":
    ascii_art()
    matches = get_current_matches()
    print('Current matches in play')
    print('=' * 23)
    
    for i, match in enumerate(matches):
        print('[{}] '.format(i) +
              re.search('\D+', match.split('v')[0]).group() + 'vs.' +
              re.search('\D+', match.split('v')[1]).group()
              )

    print()
    matchNum = int(input('Pick the match number [0, 1, 2...] => '))

    # Show desktop notification every 30 seconds
    while True:
        current_score = fetch_score(matchNum)
        notify(current_score)
        sleep(10)
