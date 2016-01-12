import math
import scipy.stats
import itertools
import scrapeGameLogs
from scrapeGameLogs import getPlayerStats
from players import players
import copy
import operator

Austin = ['John Wall', 'Jrue Holiday', 'Thaddeus Young', 'Tobias Harris', 'Tim Duncan', 'Evan Fournier', 'Kevin Love', 'DeMarcus Cousins', 'Rudy Gay', 'Eric Gordon', 'Marc Gasol', 'Jahlil Okafor', 'Avery Bradley']
Austin2 = ['Damian Lillard', 'Jrue Holiday', 'Thaddeus Young', 'Giannis Antetokounmpo', 'Tim Duncan', 'Evan Fournier', 'Gordon Hayward', 'Andre Drummond', 'Al Horford', 'Eric Gordon', 'Marc Gasol', 'Jahlil Okafor', 'Avery Bradley']
Wayland = ['Stephen Curry', 'Brandon Knight', 'Kentavious Caldwell-Pope', 'Zach Randolph', 'Serge Ibaka', 'Kemba Walker', 'Nikola Jokic', 'Kyrie Irving', 'Elfrid Payton', 'Monta Ellis', 'Blake Griffin', 'Mike Conley', 'Will Barton']
Sam = ['Goran Dragic', 'Nicolas Batum', 'Robert Covington', 'Julius Randle', 'Greg Monroe', 'Andrew Wiggins', 'Kawhi Leonard', 'Russell Westbrook', 'Chris Bosh', 'George Hill', 'Carmelo Anthony', 'Kyle Korver', 'Kristaps Porzingis']
Raymond = ['Rajon Rondo', 'Victor Oladipo', 'Kevin Durant', 'Paul George', 'Karl-Anthony Towns', 'Reggie Jackson', 'Kobe Bryant', 'Dwyane Wade', 'Jordan Clarkson', 'Nikola Vucevic', 'Danilo Gallinari', 'Wesley Matthews', 'Harrison Barnes']
Jeremy = ['Chris Paul', 'Kyle Lowry', 'Jae Crowder', 'LaMarcus Aldridge', 'DeAndre Jordan', 'Ricky Rubio', 'Pau Gasol', 'Terrence Jones', 'Gorgui Dieng', 'Tony Parker', 'Deron Williams', 'Derrick Favors', 'Zaza Pachulia']
Travis = ['Damian Lillard', 'Tyreke Evans', 'LeBron James', 'Al Horford', 'Andre Drummond', 'Gordon Hayward', 'Trevor Ariza', 'Draymond Green', 'Dirk Nowitzki', 'Marcin Gortat', 'Giannis Antetokounmpo', 'Omri Casspi', 'Kent Bazemore']
Travis2 = ['John Wall', 'Tyreke Evans', 'LeBron James', 'Kevin Love', 'DeMarcus Cousins', 'Rudy Gay', 'Trevor Ariza', 'Draymond Green', 'Dirk Nowitzki', 'Marcin Gortat', 'Tobias Harris', 'Omri Casspi', 'Kent Bazemore']
Gabe = ['C.J. McCollum', 'James Harden', 'Klay Thompson', 'Hassan Whiteside', 'Al Jefferson', 'Isaiah Thomas', 'Kenneth Faried', 'Nerlens Noel', 'Jarrett Jack', 'J.J. Redick', 'Dwight Howard', 'Arron Afflalo']
Hashmi = ['Michael Carter-Williams', 'Jimmy Butler', 'Ryan Anderson', 'Anthony Davis', 'Brook Lopez', 'Jeff Teague', 'Paul Millsap', 'Khris Middleton', 'Bradley Beal', 'David Lee', 'Jonas Valanciunas', 'DeMar DeRozan', 'Enes Kanter']
allPlayers = [Austin2, Wayland, Sam, Raymond, Jeremy, Travis2]
allPlayerNames = ['Austin', 'Wayland', 'Sam', 'Raymond', 'Jeremy', 'Travis']
usedAgents = Austin + Wayland + Sam + Raymond + Jeremy + Travis + Gabe + Hashmi
freeAgents = [agent for agent in players if agent not in usedAgents]
playerNamesPointguards = {}
for index, player in enumerate(allPlayers):
	playerNamesPointguards[player[0]] = allPlayerNames[index]

cache = {}

# Function: probWin
# -------------------------
# Determines the probability that myPlayers will win more categories than oppPlayers assuming that each of them play numDaysPerPlayer number of days
def probWin(myPlayers, oppPlayers, numDaysPerPlayer=3): 
	probWinningCategory = {}
	myPlayerCategories = {}
	oppPlayerCategories = {}
	myPlayerStats = []
	oppPlayerStats = []
	for player in myPlayers:
		if player in cache:
			stats = cache[player]
		else:
			stats = getPlayerStats(player)
			cache[player] = stats
		[myPlayerStats.append(stats) for i in range(numDaysPerPlayer)]
	for player in oppPlayers:
		if player in cache:
			stats = cache[player]
		else:
			stats = getPlayerStats(player)
			cache[player] = stats
		[oppPlayerStats.append(stats) for i in range(numDaysPerPlayer)]
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
		#print 'Probability of winning %s: %f' % (category, probWinningCategory[category])
	#print 'myPlayerCategories: ',myPlayerCategories
	#print 'oppPlayerCategories: ', oppPlayerCategories
	netDifference = {}
	for category in myPlayerCategories:
		netDifference[category] = myPlayerCategories[category][0] - oppPlayerCategories[category][0]
	#print 'Net difference: ', netDifference

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
	#print 'Probability of winning more categories overall: ', probWinning
	return probWinning

# Function: probWinningAgainstOpponents
# -------------------------
# Determines the average probability that the playerLineup will win against all opponents by calling probWin for all other players and averaging
def probWinningAgainstOpponents(player, playerLineup):
	#Make opponents the list of everyone except yourself, i.e. for me it would be Austin, Wayland, Sam, Raymond, Jeremy
	opponents = copy.deepcopy(allPlayers)
	opponents.remove(player)
	#print playerNamesPointguards[player[0]] + ': '
	#Make this list the same thing as opponents except with quotation marks around the names
	#opponentNames = [x for x in allPlayerNames if x != playerNamesPointguards[player[0]]]
	averageProbWin = 0
	for index, opponent in enumerate(opponents):
		probabilityWin = probWin(playerLineup, opponent)
		#print 'vs ' + opponent[0] + ': '
		averageProbWin += probabilityWin
	averageProbWin = averageProbWin/len(opponents)
	#print 'Average probability of winning: ' + str(averageProbWin)
	return averageProbWin

# Function: evaluateTrade
# -------------------------
# Evaluates the effect that a trade involving player1PlayersToTrade and player2PlayersToTrade will have on both players
def evaluateTrade(player1, player2, player1PlayersToTrade, player2PlayersToTrade):
	if not set(player1PlayersToTrade).issubset(set(player1)) or not set(player2PlayersToTrade).issubset(set(player2)):
		#print 'Players specified in the trade are not owned by the players'
		return 

	player1Opponents = copy.deepcopy(allPlayers)
	player1Opponents.remove(player1)

	player2Opponents = copy.deepcopy(allPlayers)
	player2Opponents.remove(player2)

	print '#### Evaluating ' + playerNamesPointguards[player1[0]] + '\'s and ' + playerNamesPointguards[player2[0]] + '\'s trade of ' + str(player1PlayersToTrade) + ' for ' + str(player2PlayersToTrade) + ' ####'
	'''
	print
	print '---For ' + playerNamesPointguards[player1[0]] + ' pre-trade---'
	'''
	averageProbWin = 0
	for index, opponent in enumerate(player1Opponents):
		probWinning = probWin(player1, opponent)
		'''
		print 'Probability of winning vs ' + playerNamesPointguards[opponent[0]] + ': ' + str(probWinning)
		'''
		averageProbWin += probWinning
	'''
	print
	'''
	player1ProbWinning_pretrade = averageProbWin/len(player1Opponents)
	'''
	print 'Average pre-trade probability of winning: ', player1ProbWinning_pretrade

	print
	print '---For ' + playerNamesPointguards[player2[0]] + ' pre-trade---'
	'''
	averageProbWin = 0
	for index, opponent in enumerate(player2Opponents):
		probWinning = probWin(player2, opponent)
		#print 'Probability of winning vs ' + playerNamesPointguards[opponent[0]] + ': ' + str(probWinning)
		averageProbWin += probWinning
	'''
	print
	'''
	player2ProbWinning_pretrade = averageProbWin/len(player1Opponents)
	'''
	print 'Average pre-trade probability of winning: ', player2ProbWinning_pretrade
	'''
	player1PostTrade = [x for x in player1 if x not in player1PlayersToTrade]
	player1PostTrade += player2PlayersToTrade

	player2PostTrade = [x for x in player2 if x not in player2PlayersToTrade]
	player2PostTrade += player1PlayersToTrade

	player1Opponents.remove(player2)
	player1Opponents.append(player2PostTrade)

	player2Opponents.remove(player1)
	player2Opponents.append(player1PostTrade)

	'''
	print
	print '---For ' + playerNamesPointguards[player1[0]] + ' post-trade---'
	'''
	averageProbWin = 0
	for index, opponent in enumerate(player1Opponents):
		if index == len(player1Opponents) - 1:
			name = playerNamesPointguards[player2[0]]
		else:
			name = playerNamesPointguards[opponent[0]]
		probWinning = probWin(player1PostTrade, opponent)
		'''
		print 'Probability of winning vs ' + name + ': ' + str(probWinning)
		'''
		averageProbWin += probWinning
	#print
	player1ProbWinning_posttrade = averageProbWin/len(player1Opponents)
	'''
	print 'Average post-trade probability of winning: ', player1ProbWinning_posttrade

	print
	print '---For ' + playerNamesPointguards[player2[0]] + ' post-trade---'
	'''
	averageProbWin = 0
	for index, opponent in enumerate(player2Opponents):
		if index == len(player2Opponents) - 1:
			name = playerNamesPointguards[player1[0]]
		else:
			name = playerNamesPointguards[opponent[0]]
		probWinning = probWin(player2PostTrade, opponent)
		#print 'Probability of winning vs ' + name + ': ' + str(probWinning)
		averageProbWin += probWinning
	#print
	player2ProbWinning_posttrade = averageProbWin/len(player1Opponents)
	#print 'Average post-trade probability of winning: ', player2ProbWinning_posttrade

	'''
	print
	print 'Trade increased ' + str(playerNamesPointguards[player1[0]]) + '\'s average probability of winning by ' + str(player1ProbWinning_posttrade - player1ProbWinning_pretrade) + ' from ' + str(player1ProbWinning_pretrade) + ' to ' + str(player1ProbWinning_posttrade)
	print 'Trade increased ' + str(playerNamesPointguards[player2[0]]) + '\'s average probability of winning by ' + str(player2ProbWinning_posttrade - player2ProbWinning_pretrade) + ' from ' + str(player2ProbWinning_pretrade) + ' to ' + str(player2ProbWinning_posttrade)
	'''
	return (player1ProbWinning_posttrade - player1ProbWinning_pretrade, player2ProbWinning_posttrade - player2ProbWinning_pretrade)

# Function: findMutuallyBeneficialTrade
# -------------------------
# Calls evaluateTrade on all possible one-player and two-player trades to see which trades are net beneficial to both sides
def findMutuallyBeneficialTrade(player1, player2):
	mutuallyBeneficialTrades = {}
	#one player trades 
	oneplayer_trades = list(itertools.product(player1, player2))
	for trade in oneplayer_trades:
		#print trade
		tradeImpact = evaluateTrade(player1, player2, [trade[0]], [trade[1]])
		if tradeImpact[0] > 0 and tradeImpact[1] > 0:
			mutuallyBeneficialTrades[trade] = tradeImpact

	twoplayer_trades = list(itertools.product(itertools.combinations(player1, 2), itertools.combinations(player2, 2)))
	for trade in twoplayer_trades:
		#print trade
		tradeImpact = evaluateTrade(player1, player2, [x for x in trade[0]], [x for x in trade[1]])
		if tradeImpact[0] > 0 and tradeImpact[1] > 0:
			mutuallyBeneficialTrades[trade] = tradeImpact

	print mutuallyBeneficialTrades
	return mutuallyBeneficialTrades

# Function: findGoodFreeAgents
# -------------------------
# Goes through all the players that are not currently on a team and returns the agents that would be net beneficial to a given player
def findGoodFreeAgents(player1):
	goodPickups = {}
	for player in player1:
		for fa in freeAgents:
			newLineup = copy.deepcopy(player1)
			newLineup.remove(player)
			newLineup.append(fa)
			probOld = probWinningAgainstOpponents(player1, player1)
			probNew = probWinningAgainstOpponents(player1, newLineup)
			if probNew > probOld:
				goodPickup = (player, fa)
				goodPickups[goodPickup] = probNew - probOld
	sorted_pickups = sorted(goodPickups.items(), key=operator.itemgetter(1), reverse=True)
	print sorted_pickups
	return sorted_pickups

# Function: probWin_v2
# -------------------------
# version 2 of the probWin function that calculates the probability of winning given current stats a certain point in the week
def probWin_v2(myCurrStats, oppCurrStats, myPlayersLeft, oppPlayersLeft):
		probWinningCategory = {}
		myPlayerCategories = {}
		oppPlayerCategories = {}
		myPlayerStats = []
		oppPlayerStats = []
		for player in myPlayersLeft:
			if player in cache:
				stats = cache[player]
			else:
				stats = getPlayerStats(player)
				cache[player] = stats
			myPlayerStats.append(stats)
		for player in oppPlayersLeft:
			if player in cache:
				stats = cache[player]
			else:
				stats = getPlayerStats(player)
				cache[player] = stats
			oppPlayerStats.append(stats)
		categories = {'FG%': '+', 'FT%': '+', '3PM': '+', 'REB': '+', 'AST': '+', 'STL': '+', 'BLK': '+', 'TO': '-', 'PTS': '+'}
		for category, plusOrMinus in categories.iteritems():
			myMean = 0
			myStd = 0
			if category == 'FG%':
				totalFGAttempted = sum([player['FGA'][0] for player in myPlayerStats]) + myCurrStats['FGA']
			elif category == 'FT%':
				totalFTAttempted = sum([player['FTA'][0] for player in myPlayerStats]) + myCurrStats['FTA']
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
				myMean += myCurrStats['FGM']
				myMean /= totalFGAttempted
				myStd /= totalFGAttempted
			elif category == 'FT%':
				myMean += myCurrStats['FTM']
				myMean /= totalFTAttempted
				myStd /= totalFTAttempted
			else:
				myMean += myCurrStats[category]	
			myPlayerCategories[category] = (myMean, myStd)

			oppMean = 0
			oppStd = 0
			if category == 'FG%':
				totalFGAttempted = sum([player['FGA'][0] for player in oppPlayerStats]) + oppCurrStats['FGA']
			elif category == 'FT%':
				totalFTAttempted = sum([player['FTA'][0] for player in oppPlayerStats]) + oppCurrStats['FTA']
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
				oppMean += oppCurrStats['FGM']
				oppMean /= totalFGAttempted
				oppStd /= totalFGAttempted
			elif category == 'FT%':
				oppMean += oppCurrStats['FTM']
				oppMean /= totalFTAttempted
				oppStd /= totalFTAttempted
			else:
				oppMean += oppCurrStats[category]	
			oppPlayerCategories[category] = (oppMean, oppStd)

			differenceMean = myMean - oppMean
			differenceStd = math.sqrt(oppStd**2 + myStd**2)

			if plusOrMinus == '+':
				probWinningCategory[category] = 1.0 - scipy.stats.norm(differenceMean, differenceStd).cdf(0)
			elif plusOrMinus == '-':
				probWinningCategory[category] = scipy.stats.norm(differenceMean, differenceStd).cdf(0)
			#print 'Probability of winning %s: %f' % (category, probWinningCategory[category])
		#print 'myPlayerCategories: ',myPlayerCategories
		#print 'oppPlayerCategories: ', oppPlayerCategories
		netDifference = {}
		for category in myPlayerCategories:
			netDifference[category] = myPlayerCategories[category][0] - oppPlayerCategories[category][0]
		#print 'Net difference: ', netDifference

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
		return probWinning

# Function: setLineup
# -------------------------
# Gives recommendations on which players to play given my current stats and opponent current stats
def setLineup(myCurrStats, oppCurrStats, myPlayersLeft, oppPlayersLeft):
	maxProb = 0.0
	maxLineup = None
	for size in range(0, len(myPlayersLeft) + 1):
		for subset in itertools.combinations(myPlayersLeft, size):
			prob = probWin_v2(myCurrStats, oppCurrStats, list(subset), oppPlayersLeft) 
			if prob > maxProb:
				maxProb = prob
				maxLineup = list(subset)
	return (maxLineup, maxProb)
	
#example commands
'''
findMutuallyBeneficialTrade(Travis2, Austin2)
evaluateTrade(Travis2, Wayland, ['Dirk Nowitzki'], ['Serge Ibaka'])
print probWin(Travis2, Austin2)
evaluateTrade(Travis, Austin, ['Damian Lillard'], ['John Wall'])
findGoodFreeAgents(Travis)
myCurrStats = {'FGM': 147, 'FGA': 344, 'FTM': 79, 'FTA': 107, '3PM': 45, 'REB': 200, 'AST': 83, 'STL': 27, 'BLK': 17, 'TO': 52, 'PTS': 418}
gabeCurrStats = {'FGM': 178, 'FGA': 338, 'FTM': 87, 'FTA': 118, '3PM': 42, 'REB': 182, 'AST':71, 'STL': 27, 'BLK': 27, 'TO': 68, 'PTS': 485}
print setLineup(myCurrStats, gabeCurrStats, ['Trevor Ariza', 'LeBron James', 'Draymond Green', 'DeMarcus Cousins', 'Tyreke Evans', 'Tobias Harris', 'Dirk Nowitzki', 'Omri Casspi', 'Kevin Love', 'Marcin Gortat', 'Kent Bazemore', 'John Wall'], ['J.J. Redick', 'Hassan Whiteside', 'Klay Thompson', 'Nerlens Noel', 'Kenneth Faried', 'Arron Afflalo', 'Dwight Howard', 'James Harden', 'Kenneth Faried', 'C.J. McCollum', 'Jarrett Jack', 'Isaiah Thomas'])
'''
