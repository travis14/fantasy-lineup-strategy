from bs4 import BeautifulSoup 
from urllib2 import urlopen
from time import sleep
import sys
import csv
from re import sub
from decimal import Decimal
import statistics

FULL_DEPTH_URL = "http://espn.go.com/nba/depth/_/type/full"
PLAYER_BASE_URL = "http://espn.go.com/nba/player/"
FULL_DEPTH_SOUP = BeautifulSoup(urlopen(FULL_DEPTH_URL), "lxml") 
a_hrefs = [td.find('a') for td in FULL_DEPTH_SOUP.find_all('td')] #if '1' in str(td)[4:7] or '2' in str(td)[4:7]]
player_profile_links = [a_href['href'] for a_href in a_hrefs if a_href and PLAYER_BASE_URL in a_href['href']]

def getGameLogs(name):
	nameWithHyphen = "-".join(name.lower().split())
	profile_link = next(link for link in player_profile_links if nameWithHyphen in link)
	game_log_link = profile_link.split('player', 1)[0] + 'player/gamelog' + profile_link.split('player', 1)[1]
	game_log_soup = BeautifulSoup(urlopen(game_log_link), 'lxml')
	table = game_log_soup.find_all('table')[1]
	rows = table.find_all('tr')
	categories = [row.text for row in rows[1].find_all('td')]
	
getGameLogs('Marcin Gortat')

