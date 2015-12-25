import math
import scipy.stats
import itertools
import scrapeGameLogs
from scrapeGameLogs import getPlayerStats

categories = {'FG%': '+', 'FT%': '+', '3PM': '+', 'REB': '+', 'AST': '+', 'STL': '+', 'BLK': '+', 'TO': '-', 'PTS': '+'}
def probWin(myPlayers, oppPlayers): 
	probWinningCategory = {}
	myPlayerCategories = {}
	oppPlayerCategories = {}
	myPlayerStats = []
	oppPlayerStats = []
	for player in myPlayers:
		stats = getPlayerStats(player)
		myPlayerStats.append(stats)
		myPlayerStats.append(stats)
		myPlayerStats.append(stats)
	for player in oppPlayers:
		stats = getPlayerStats(player)
		oppPlayerStats.append(stats)
		oppPlayerStats.append(stats)
		oppPlayerStats.append(stats)
	categories = {'FG%': '+', 'FT%': '+', '3PM': '+', 'REB': '+', 'AST': '+', 'STL': '+', 'BLK': '+', 'TO': '-', 'PTS': '+'}
	for category, plusOrMinus in categories.iteritems():
		myMean = 0
		myStd = 0
		if category == 'FG%':
			totalFGAttempted = sum([player['FGA'][0] for player in myPlayerStats])
		elif category == 'FT%':
			totalFTAttempted = sum([player['FTA'][0] for player in myPlayerStats])
		for player in myPlayerStats:
			if category == 'FG%':
				myMean += float(player['FGM'][0])
				myStd = math.sqrt(myStd**2 + player['FGM'][1]**2)
			elif category == 'FT%':
				myMean += float(player['FTM'][0])
				myStd = math.sqrt(myStd**2 + player['FTM'][1]**2)
			else:
				myMean += float(player[category][0])
				myStd = math.sqrt(myStd**2 + player[category][1]**2)
		if category == 'FG%':
			myMean /= totalFGAttempted
			myStd /= totalFGAttempted
		elif category == 'FT%':
			myMean /= totalFTAttempted
			myStd /= totalFTAttempted	
		myPlayerCategories[category] = (myMean, myStd)

		oppMean = 0
		oppStd = 0
		if category == 'FG%':
			totalFGAttempted = sum([player['FGA'][0] for player in oppPlayerStats])
		elif category == 'FT%':
			totalFTAttempted = sum([player['FTA'][0] for player in oppPlayerStats])
		for player in oppPlayerStats:
			if category == 'FG%':
				oppMean += float(player['FGM'][0])
				oppStd = math.sqrt(oppStd**2 + player['FGM'][1]**2)
			elif category == 'FT%':
				oppMean += float(player['FTM'][0])
				oppStd = math.sqrt(oppStd**2 + player['FTM'][1]**2)
			else:
				oppMean += float(player[category][0])
				oppStd = math.sqrt(oppStd**2 + player[category][1]**2)
		if category == 'FG%':
			oppMean /= totalFGAttempted
			oppStd /= totalFGAttempted
		elif category == 'FT%':
			oppMean /= totalFTAttempted
			oppStd /= totalFTAttempted	
		oppPlayerCategories[category] = (oppMean, oppStd)
		differenceMean = myMean - oppMean
		differenceStd = math.sqrt(oppStd**2 + myStd**2)

		if plusOrMinus == '+':
			probWinningCategory[category] = 1.0 - scipy.stats.norm(differenceMean, differenceStd).cdf(0)
		elif plusOrMinus == '-':
			probWinningCategory[category] = scipy.stats.norm(differenceMean, differenceStd).cdf(0)
		print 'Probability of winning %s: %f' % (category, probWinningCategory[category])

	print 'myPlayerCategories: ', myPlayerCategories
	print 'oppPlayerCategories: ', oppPlayerCategories

	categories = probWinningCategory.keys()
	numCategories = float(len(categories))
	numCategoriesToWin = int(math.ceil(numCategories / 2.0))
	probWinning = 0
	for i in range(numCategoriesToWin, len(categories) + 1):
		combinations = list(itertools.combinations(categories, i))
		for combo in combinations:
			probWinningCombo = 1
			for category in categories:
				if category in combo:
					probWinningCombo *= probWinningCategory[category]
				else:
					probWinningCombo *= (1 - probWinningCategory[category])
			probWinning += probWinningCombo
			#print 'Probability of winning %s: %f' %(combo, probWinningCombo)
	print 'Probability of winning more categories overall: ', probWinning
	return probWinning

Austin = ['Thaddeus Young', 'Jahlil Okafor', 'Marc Gasol', 'Eric Bledsoe', 'Kevin Love', 'Tobias Harris', 'John Wall', 'DeMarcus Cousins', 'Avery Bradley', 'Marvin Williams', 'Rudy Gay', 'Tim Duncan', 'Jared Sullinger', 'Jrue Holiday']
Wayland_pretrade = ['Mike Conley', 'Brandon Knight', 'Kentavious Caldwell-Pope', 'Zach Randolph', 'Serge Ibaka', 'Kyrie Irving', 'Blake Griffin', 'Stephen Curry', 'Kemba Walker', 'Monta Ellis', 'Elfrid Payton', 'Will Barton', 'Bismack Biyombo']
Wayland_posttrade = ['Mike Conley', 'Marcin Gortat', 'Kentavious Caldwell-Pope', 'Zach Randolph', 'Serge Ibaka', 'Kyrie Irving', 'LeBron James', 'Stephen Curry', 'Kemba Walker', 'Monta Ellis', 'Elfrid Payton', 'Will Barton', 'Bismack Biyombo']
Sam = ['Goran Dragic', 'Nicolas Batum', 'Robert Covington', 'Julius Randle', 'Greg Monroe', 'Andrew Wiggins', 'Kawhi Leonard', 'Russell Westbrook', 'Chris Bosh', 'George Hill', 'Carmelo Anthony', 'Kyle Korver', 'Kristaps Porzingis']
Raymond = ['Rajon Rondo', 'Victor Oladipo', 'Kevin Durant', 'Paul George', 'Karl-Anthony Towns', 'Reggie Jackson', 'Kobe Bryant', 'Dwyane Wade', 'Jordan Clarkson', 'Nikola Vucevic', 'Danilo Gallinari', 'Wesley Matthews', 'Harrison Barnes']
Jeremy = ['Chris Paul', 'Kyle Lowry', 'Jae Crowder', 'LaMarcus Aldridge', 'DeAndre Jordan', 'Ricky Rubio', 'Pau Gasol', 'Terrence Jones', 'Gorgui Dieng', 'Tony Parker', 'Deron Williams', 'Derrick Favors', 'Zaza Pachulia']
Travis_pretrade = ['Damian Lillard', 'Tyreke Evans', 'LeBron James', 'Al Horford', 'Andre Drummond', 'Gordon Hayward', 'Trevor Ariza', 'Draymond Green', 'Dirk Nowitzki', 'Marcin Gortat', 'Giannis Antetokounmpo', 'DeMarre Carroll', 'Omri Casspi']
Travis_posttrade = ['Damian Lillard', 'Tyreke Evans', 'Blake Griffin', 'Al Horford', 'Andre Drummond', 'Gordon Hayward', 'Trevor Ariza', 'Draymond Green', 'Dirk Nowitzki', 'Brandon Knight', 'Giannis Antetokounmpo', 'DeMarre Carroll', 'Omri Casspi']

print
print '---PRE-WAYLAND TRADE---'
opponents = [Austin, Wayland_pretrade, Sam, Raymond, Jeremy]
opponentNames = ['Austin', 'Wayland_pretrade', 'Sam', 'Raymond', 'Jeremy']
averageProbWin = 0
for index, opponent in enumerate(opponents):
	print
	print 'vs ' + opponentNames[index] + ': '
	averageProbWin += probWin(Travis_pretrade, opponent)
print
print 'Average probability of winning: ', averageProbWin/len(opponentNames)

print
print '---PRE-WAYLAND TRADE---'
opponents = [Austin, Wayland_posttrade, Sam, Raymond, Jeremy]
opponentNames = ['Austin', 'Wayland_posttrade', 'Sam', 'Raymond', 'Jeremy']
averageProbWin = 0
for index, opponent in enumerate(opponents):
	print
	print 'vs ' + opponentNames[index] + ': '
	averageProbWin += probWin(Travis_posttrade, opponent)
print
print 'Average probability of winning: ', averageProbWin/len(opponentNames)



