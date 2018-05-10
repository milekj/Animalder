from exceptions import *
from providers import *

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from  matplotlib.ticker import MaxNLocator
import sys

class MatchesChartDrawer:
    def __init__(self, provider):
        self.matchesProvider = provider
        self.numbers = []

    def draw(self):

        texts, autotexts = self.drawBasic()
        self.adjustLabels(texts, autotexts)
        self.addTitle()
        plt.show()

    def drawBasic(self):
        try:
            playedNumber = self.matchesProvider.getPlayed()
            wonNumber = self.matchesProvider.getWon()
            lostNumber = playedNumber - wonNumber
        except InvalidDataException as e:
            raise InvalidChartDataException('Data for matches chart is invalid. Cause: ' + str(e))

        self.numbers = [wonNumber, lostNumber]

        grid = GridSpec(1, 1)
        plt.subplot(grid[0, 0], aspect = 1)

        patches, texts, autotexts = plt.pie([wonNumber / playedNumber, lostNumber / playedNumber], 
                                                        (0.05, 0.1), 
                                                        ['won', 'lost'], 
                                                        ['tab:green', 'tab:red'], 
                                                        autopct ='%.0f%%', shadow = True)
        return texts, autotexts


    def adjustLabels(self, texts, autotexts):
        for t in texts:
            t.set_size('xx-large')

        for t, n in zip(autotexts, self.numbers):
            t.set_size('xx-large')
            t.set_text(t.get_text() + ' (' + str(n) + ')')


    def addTitle(self):
        seasonStart = self.matchesProvider.getSeason()
        seasonEnd = seasonStart + 1

        chartTitle = self.matchesProvider.getName() + \
                    ' - matches in ' + \
                    str(seasonStart) + \
                    '/' + \
                    str(seasonEnd)

        plt.title(chartTitle , {'fontsize': 'xx-large'})

class RankingChartDrawer:

    def __init__(self, provider, name):
        self.name = name
        self.rankingProvider = provider
        self.x = []
        self.y = []
        
    def draw(self):
        try:
            self.x, self.y = self.rankingProvider.getRangeRanking()
        except InvalidDataException as e:
            raise InvalidChartDataException('Data for ranking chart is invalid. Cause: ' + str(e))    

        plt.plot(self.x, self.y, 'ro-')
        self.adjustAxes()
        self.drawPointsData()        
    
    def adjustAxes(self):
        pass
        
    
    def drawPointsData(self):
        for a,b in zip(self.x, self.y):
            plt.text(a,b, str(b), size = 'large')
        plt.show()

class PositionChartDrawer(RankingChartDrawer):
    def adjustAxes(self):
        axes = plt.gca()
        axes.set_xticks(self.x)
        axes.invert_yaxis()
        axes.set_ylim(max(self.y) + 5, 0)
        axes.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.title(self.name + ' - ranking', {'fontsize': 'xx-large'})

class MoneyChartDrawer(RankingChartDrawer):
    def adjustAxes(self):
        axes = plt.gca()
        axes.yaxis.set_major_locator(MaxNLocator(integer=True))
        axes.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.title(self.name + ' - prize money [£]', {'fontsize': 'xx-large'})
