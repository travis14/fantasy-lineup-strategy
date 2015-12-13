import math
import scipy.stats
import itertools

# Class: CurrentStatistics
# -------------------------
# Represents both players stats in the current state of the game 
class CurrentStatistics:
	def __init__(self, categories, myCategories, oppCategories):
		assert(set(categories.keys()) == set(myCategories.keys()) and set(categories.keys()) == set(oppCategories.keys()))
		assert(value == '+' or value == '-' or value == '%' for key, value in categories.iteritems())
		self.categories = categories
		self.myCategories = myCategories
		self.oppCategories = oppCategories

	#assumes my players is a dictionary from the category to (mean, std) tuples
	def probWinOneDay(self, myPlayers, oppPlayers): 
		assert(all(set(myPlayer.keys()) == set(oppPlayer.keys()) and set(myPlayer.keys()) == set(self.categories.keys()) for myPlayer in myPlayers for oppPlayer in oppPlayers))
		probWinningCategory = {}
		myPlayerCategories = {}
		oppPlayerCategores = {}
		for category, plusOrMinusOrPercent in self.categories.iteritems():
			myMean = 0
			myStd = 0
			for player in myPlayers:
				myMean += float(player[category][0])
				myStd = math.sqrt(myStd**2 + player[category][1]**2)
			myPlayerCategories[category] = (myMean, myStd)

			oppMean = 0
			oppStd = 0
			for player in oppPlayers:
				oppMean += float(player[category][0])
				oppStd = math.sqrt(oppStd**2 + player[category][1]**2)

			differenceMean = self.myCategories[category] - self.oppCategories[category] + myMean - oppMean
			differenceStd = math.sqrt(oppStd**2 + myStd**2)

			if plusOrMinus == '+':
				probWinningCategory[category] = 1.0 - scipy.stats.norm(differenceMean, differenceStd).cdf(0)
			elif plusOrMinus == '-':
				probWinningCategory[category] = scipy.stats.norm(differenceMean, differenceStd).cdf(0)
			print 'Probability of winning %s: %f' % (category, probWinningCategory[category])

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
				print 'Probability of winning %s: %f' %(combo, probWinningCombo)
		print 'Probability of winning more categories overall: ', probWinning


categories = {'3PM': '+', 'REB': '+', 'AST': '+', 'STL': '+', 'BLK': '+', 'TO': '-', 'PTS': '+'}
me = {'3PM': 40, 'REB': 294, 'AST': 140, 'STL': 56, 'BLK': 36, 'TO': 93, 'PTS': 612}
austin = {'3PM': 35, 'REB': 286, 'AST': 134, 'STL': 47, 'BLK': 26, 'TO': 93, 'PTS': 624}
test = CurrentStatistics(categories, me, austin)

player1 = {'3PM': (2.0, .6), 'REB': (5.1, 2), 'AST': (3.3, 1),  'STL': (1.2, .5), 'BLK': (.1, .01), 'TO': (2.4, 1), 'PTS': (18.9, 5)}
player5 = {'3PM': (0, 0), 'REB': (7.5, 2), 'AST': (0.2, 0.02),  'STL': (0.2, 0.04), 'BLK': (1.1, .2), 'TO': (.6, .3), 'PTS': (5.1, 1.3)}
player2 = {'3PM': (1.8, .7), 'REB': (4.2, 1.9), 'AST': (6.3, 2.5),  'STL': (2.0, .5), 'BLK': (.6, .2), 'TO': (2.8, 1), 'PTS': (22.3, 3.4)}
player3 = {'3PM': (0.1, .001), 'REB': (7.7, 3), 'AST': (3.8, 1.7),  'STL': (0.7, .1), 'BLK': (1.2, .2), 'TO': (2.2, .4), 'PTS': (16.3, 5)}
player4 = {'3PM': (0.0, 0.0), 'REB': (7.9, 3), 'AST': (1.3, .2),  'STL': (0.3, .05), 'BLK': (1.5, .5), 'TO': (3, .5), 'PTS': (17.3, 6)}
test.probWinOneDay([player1, player5], [player2, player3, player4])







