from bs4 import BeautifulSoup 
from urllib2 import urlopen
from time import sleep
import sys
import csv
from re import sub
from decimal import Decimal
from players import players
import statistics
import scipy.stats

FULL_DEPTH_URL = "http://espn.go.com/nba/depth/_/type/full"
PLAYER_BASE_URL = "http://espn.go.com/nba/player/"
FULL_DEPTH_SOUP = BeautifulSoup(urlopen(FULL_DEPTH_URL), "lxml") 
a_hrefs = [td.find('a') for td in FULL_DEPTH_SOUP.find_all('td')] #if '1' in str(td)[4:7] or '2' in str(td)[4:7]]
player_profile_links = [a_href['href'] for a_href in a_hrefs if a_href and PLAYER_BASE_URL in a_href['href']]

# Function: getGameLogs
# -------------------------
# Returns a list of game logs for a player given his/her name
# Game logs are in the form of dictionaries of category to value, i.e. {'PTS': 15.0, 'REB': 8.0, ...}
def getGameLogs(name):
	nameWithHyphen = "-".join(name.lower().split())
	try:
		profile_link = next(link for link in player_profile_links if nameWithHyphen in link)
	except:
		print 'name with error: ', name
	game_log_link = profile_link.split('player', 1)[0] + 'player/gamelog' + profile_link.split('player', 1)[1]
	try:
		game_log_soup = BeautifulSoup(urlopen(game_log_link), 'lxml')
		table = game_log_soup.find_all('table')[1]
		rows = table.find_all('tr')
		categories = [row.text for row in rows[1].find_all('td')]
	except:
		print 'game log with error: ', game_log_link
		#print categories
	logs = []
	for row in rows:
		if 'PRESEASON' in row.find('td').text:
			break
		#relevant rows have a class tag of ['oddrow', 'team-46-28'], for example
		if len(row['class']) == 2: 
			log = {}
			for index, stat in enumerate(row.find_all('td')):
				category = categories[index]
				log[category] = stat.text
			logs.append(log)
	return logs

# Function: getPlayerStats
# -------------------------
# From the game logs of a given player, returns a dictionary of category to (mean, standard deviation) tuples
def getPlayerStats(name):
	gameLogs = getGameLogs(name)
	numGames = 0
	formattedGameLogs = []
	for log in gameLogs:
		if int(log['MIN']) > 0:
			formattedLog = {}
			formattedLog['FGM-FGA'] = (float(log['FGM-FGA'].split('-')[0]), float(log['FGM-FGA'].split('-')[1]))
			formattedLog['FTM-FTA'] = (float(log['FTM-FTA'].split('-')[0]), float(log['FTM-FTA'].split('-')[1])) 
			formattedLog['3PM'] = float(log['3PM-3PA'].split('-')[0])
			formattedLog['REB'] = float(log['REB'])
			formattedLog['AST'] = float(log['AST'])
			formattedLog['STL'] = float(log['STL'])
			formattedLog['BLK'] = float(log['BLK'])
			formattedLog['TO'] = float(log['TO'])
			formattedLog['PTS'] = float(log['PTS'])
			formattedGameLogs.append(formattedLog)
			numGames += 1
	if len(formattedGameLogs) < 2:
		return {'FGM': (0.0, 0.0), 'FGA': (0.0, 0.0), 'FTM': (0.0, 0.0), 'FTA': (0.0, 0.0), '3PM': (0.0, 0.0), 'REB': (0.0, 0.0), 'AST': (0.0, 0.0), 'STL': (0.0, 0.0), 'BLK':(0.0, 0.0), 'TO': (0.0, 0.0), 'PTS': (0.0, 0.0)}
	fgms = [log['FGM-FGA'][0] for log in formattedGameLogs]
	fgas = [log['FGM-FGA'][1] for log in formattedGameLogs]
	ftms = [log['FTM-FTA'][0] for log in formattedGameLogs]
	ftas = [log['FTM-FTA'][1] for log in formattedGameLogs]
	threepms = [log['3PM'] for log in formattedGameLogs]
	rebs = [log['REB'] for log in formattedGameLogs]
	asts = [log['AST'] for log in formattedGameLogs]
	stls = [log['STL'] for log in formattedGameLogs]
	blks = [log['BLK'] for log in formattedGameLogs]
	tos = [log['TO'] for log in formattedGameLogs]
	pts = [log['PTS'] for log in formattedGameLogs]
	fgm_stats = (statistics.mean(fgms), statistics.stdev(fgms))
	fga_stats = (statistics.mean(fgas), statistics.stdev(fgas))
	ftm_stats = (statistics.mean(ftms), statistics.stdev(ftms))
	fta_stats = (statistics.mean(ftas), statistics.stdev(ftas))
	threepm_stats = (statistics.mean(threepms), statistics.stdev(threepms))
	reb_stats = (statistics.mean(rebs), statistics.stdev(rebs))
	ast_stats = (statistics.mean(asts), statistics.stdev(asts))
	stl_stats = (statistics.mean(stls), statistics.stdev(stls))
	blk_stats = (statistics.mean(blks), statistics.stdev(blks))
	to_stats = (statistics.mean(tos), statistics.stdev(tos))
	pts_stats = (statistics.mean(pts),  statistics.stdev(pts))
	return {'FGM': fgm_stats, 'FGA': fga_stats, 'FTM': ftm_stats, 'FTA': fta_stats, '3PM': threepm_stats, 'REB': reb_stats, 'AST': ast_stats, 'STL': stl_stats, 'BLK':blk_stats, 'TO': to_stats, 'PTS': pts_stats}
