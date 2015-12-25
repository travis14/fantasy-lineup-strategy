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

def getGameLogs(name):
	nameWithHyphen = "-".join(name.lower().split())
	profile_link = next(link for link in player_profile_links if nameWithHyphen in link)
	game_log_link = profile_link.split('player', 1)[0] + 'player/gamelog' + profile_link.split('player', 1)[1]
	game_log_soup = BeautifulSoup(urlopen(game_log_link), 'lxml')
	table = game_log_soup.find_all('table')[1]
	rows = table.find_all('tr')
	categories = [row.text for row in rows[1].find_all('td')]
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
	fgms = [log['FGM-FGA'][0] for log in formattedGameLogs]
	fgas = [log['FGM-FGA'][1] for log in formattedGameLogs]
	ftms = [log['FGM-FGA'][0] for log in formattedGameLogs]
	ftas = [log['FGM-FGA'][1] for log in formattedGameLogs]
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
	blk_stats = (statistics.mean(stls), statistics.stdev(blks))
	to_stats = (statistics.mean(tos), statistics.stdev(tos))
	pts_stats = (statistics.mean(pts),  statistics.stdev(pts))
	return {'FGM': fgm_stats, 'FGA': fga_stats, 'FTM': ftm_stats, 'FTA': fta_stats, '3PM': threepm_stats, 'REB': reb_stats, 'AST': ast_stats, 'STL': stl_stats, 'BLK':blk_stats, 'TO': to_stats, 'PTS': pts_stats}

'''
	print 'Player: ', player
	gameLogs = getGameLogs(player)
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
	
	print 'numGames: ', numGames
	fgpcts = [log['FGM-FGA'][0]/log['FGM-FGA'][1]  for log in formattedGameLogs]
	fgms = [log['FGM-FGA'][0] for log in formattedGameLogs]
	fgas = [log['FGM-FGA'][1] for log in formattedGameLogs]
	ftms = [log['FGM-FGA'][0] for log in formattedGameLogs]
	ftas = [log['FGM-FGA'][1] for log in formattedGameLogs]
	threepms = [log['3PM'] for log in formattedGameLogs]
	rebs = [log['REB'] for log in formattedGameLogs]
	asts = [log['AST'] for log in formattedGameLogs]
	stls = [log['STL'] for log in formattedGameLogs]
	blks = [log['BLK'] for log in formattedGameLogs]
	tos = [log['TO'] for log in formattedGameLogs]
	pts = [log['PTS'] for log in formattedGameLogs]
	fgpct_stats = (statistics.mean(fgpcts), statistics.median(fgpcts), statistics.stdev(fgpcts))
	print 'FGPCT (mean, median, stdev) = ', fgpct_stats
	fgm_stats = (statistics.mean(fgms), statistics.median(fgms), statistics.stdev(fgms))
	all_fgm_stats.append(fgm_stats)
	print 'FGM (mean, median, stdev) = ', fgm_stats
	fga_stats = (statistics.mean(fgas), statistics.median(fgas), statistics.stdev(fgas))
	all_fga_stats.append(fga_stats)
	print 'FGA (mean, median, stdev) = ', fga_stats
	ftm_stats = (statistics.mean(ftms), statistics.median(ftms), statistics.stdev(ftms))
	all_ftm_stats.append(ftm_stats)
	print 'FTM (mean, median, stdev) = ', ftm_stats
	fta_stats = (statistics.mean(ftas), statistics.median(ftas), statistics.stdev(ftas))
	all_fta_stats.append(fta_stats)
	print 'FTA (mean, median, stdev) = ', fta_stats
	threepm_stats = (statistics.mean(threepms), statistics.median(threepms), statistics.stdev(threepms))
	all_3pm_stats.append(threepm_stats)
	print '3PM (mean, median, stdev) = ', threepm_stats
	reb_stats = (statistics.mean(rebs), statistics.median(rebs), statistics.stdev(rebs))
	all_reb_stats.append(reb_stats)
	print 'REB (mean, median, stdev) = ', reb_stats
	ast_stats = (statistics.mean(asts), statistics.median(asts), statistics.stdev(asts))
	all_ast_stats.append(ast_stats)
	print 'AST (mean, median, stdev) = ', ast_stats
	stl_stats = (statistics.mean(stls), statistics.median(stls), statistics.stdev(stls))
	all_stl_stats.append(stl_stats)
	print 'STL (mean, median, stdev) = ', stl_stats
	blk_stats = (statistics.mean(stls), statistics.median(blks), statistics.stdev(blks))
	all_blk_stats.append(blk_stats)
	print 'BLK (mean, median, stdev) = ', blk_stats
	to_stats = (statistics.mean(tos), statistics.median(tos), statistics.stdev(tos))
	all_to_stats.append(to_stats)
	print 'TO (mean, median, stdev) = ', to_stats
	pts_stats = (statistics.mean(pts), statistics.median(pts), statistics.stdev(pts))
	all_pts_stats.append(pts_stats)
	print 'PTS (mean, median, stdev) = ', pts_stats

all_fgm_stats = []
all_fga_stats = []
all_ftm_stats = []
all_fta_stats = []
all_3pm_stats = []
all_reb_stats = []
all_ast_stats = []
all_stl_stats = []
all_blk_stats = []
all_to_stats = []
all_pts_stats = []

for player in players:
	print 'Player: ', player
	gameLogs = getGameLogs(player)
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

	print 'numGames: ', numGames
	fgms = [log['FGM-FGA'][0] for log in formattedGameLogs]
	fgas = [log['FGM-FGA'][1] for log in formattedGameLogs]
	ftms = [log['FGM-FGA'][0] for log in formattedGameLogs]
	ftas = [log['FGM-FGA'][1] for log in formattedGameLogs]
	threepms = [log['3PM'] for log in formattedGameLogs]
	rebs = [log['REB'] for log in formattedGameLogs]
	asts = [log['AST'] for log in formattedGameLogs]
	stls = [log['STL'] for log in formattedGameLogs]
	blks = [log['BLK'] for log in formattedGameLogs]
	tos = [log['TO'] for log in formattedGameLogs]
	pts = [log['PTS'] for log in formattedGameLogs]

	fgm_stats = (statistics.mean(fgms), statistics.median(fgms), statistics.stdev(fgms))
	all_fgm_stats.append(fgm_stats)
	print 'FGM (mean, median, stdev) = ', fgm_stats
	fga_stats = (statistics.mean(fgas), statistics.median(fgas), statistics.stdev(fgas))
	all_fga_stats.append(fga_stats)
	print 'FGA (mean, median, stdev) = ', fga_stats
	ftm_stats = (statistics.mean(ftms), statistics.median(ftms), statistics.stdev(ftms))
	all_ftm_stats.append(ftm_stats)
	print 'FTM (mean, median, stdev) = ', ftm_stats
	fta_stats = (statistics.mean(ftas), statistics.median(ftas), statistics.stdev(ftas))
	all_fta_stats.append(fta_stats)
	print 'FTA (mean, median, stdev) = ', fta_stats
	threepm_stats = (statistics.mean(threepms), statistics.median(threepms), statistics.stdev(threepms))
	all_3pm_stats.append(threepm_stats)
	print '3PM (mean, median, stdev) = ', threepm_stats
	reb_stats = (statistics.mean(rebs), statistics.median(rebs), statistics.stdev(rebs))
	all_reb_stats.append(reb_stats)
	print 'REB (mean, median, stdev) = ', reb_stats
	ast_stats = (statistics.mean(asts), statistics.median(asts), statistics.stdev(asts))
	all_ast_stats.append(ast_stats)
	print 'AST (mean, median, stdev) = ', ast_stats
	stl_stats = (statistics.mean(stls), statistics.median(stls), statistics.stdev(stls))
	all_stl_stats.append(stl_stats)
	print 'STL (mean, median, stdev) = ', stl_stats
	blk_stats = (statistics.mean(stls), statistics.median(blks), statistics.stdev(blks))
	all_blk_stats.append(blk_stats)
	print 'BLK (mean, median, stdev) = ', blk_stats
	to_stats = (statistics.mean(tos), statistics.median(tos), statistics.stdev(tos))
	all_to_stats.append(to_stats)
	print 'TO (mean, median, stdev) = ', to_stats
	pts_stats = (statistics.mean(pts), statistics.median(pts), statistics.stdev(pts))
	all_pts_stats.append(pts_stats)
	print 'PTS (mean, median, stdev) = ', pts_stats

print 'all_fgm_stats: ', all_fgm_stats
print 'all_fga_stats: ', all_fga_stats
print all_ftm_stats 
print all_fta_stats
print all_3pm_stats
print all_reb_stats 
print all_ast_stats 
print all_stl_stats 
print all_blk_stats 
print all_to_stats 
print all_pts_stats 
'''
