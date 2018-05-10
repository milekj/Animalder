from providers import *
from exceptions import *
from charts import *

class ConsoleRunner:
    def __init__(self, height = 30):
        self.height = height
        self.minSeason = 2013
        self.maxSeason = 2017
    
    def run(self):
        pass
    
    def choosePlayer(self, players):
        finder = PlayerFinder(players)
        print('Enter name or part of name you wish to find: ')
        self.printEnters(2)

        name = input()
        self.printEnters(1)

        matchingPlayers = finder.getMatchingPlayers(name)

        if not matchingPlayers:
            raise InputParseException('No matching players')

        lines = self.printMatchingNames(matchingPlayers)

        self.printEnters(lines + 1)
        id = int(input('Enter number corresponding to the chosen player: '))
        self.printEnters(1)

        return matchingPlayers[id]['id'], matchingPlayers[id]['fullName']

    def printMatchingNames(self, players):
        i = 0
        for p in players:
            if (i >= self.height - 2):
                break
            print(str(i) + ': ' + p['fullName'])
            i += 1

        return i

    def loadPlayersData(self, season):
        provider = PlayersDataProvider(season)
        print('Loading players data...')
        self.printEnters(2)
        provider.init()
        return provider
        

    def printEnters(self, lines):
        n = self.height - lines
        while n > 0:
            print('')
            n -= 1
    
    def printErrorMessage(self, error):
        print(str(error))
        self.printEnters(2)
        input()
    
    def validateSeason(self, season):
        return season >= self.minSeason and season <= self.maxSeason

class MatchesRunner(ConsoleRunner):
    def run(self):
        try:
            season = self.chooseSeason()
            playersProvider = self.loadPlayersData(season)
            playerID, name = self.choosePlayer(playersProvider)
            matchesProvider = MatchesDataProvider(playerID, season, name)
            print('Loading players data...')
            self.printEnters(2)
            matchesProvider.init()
            drawer = MatchesChartDrawer(matchesProvider)
            drawer.draw()
        except (InputParseException, InvalidDataException, InvalidChartDataException) as e:
            self.printErrorMessage(e)
            return

        
        

    def chooseSeason(self):
        print('Enter season you\'re interested in (2013 - 2017): ')
        self.printEnters(2)

        try:
            season = int(input())

            if not self.validateSeason(season):
                raise InputParseException('Season out of range')
            
            return season

        except ValueError as e:
            raise InputParseException('Invalid season')

        

class RankingsRunner(ConsoleRunner):
    def run(self):
        try:
            start, end = self.chooseRankingSeasons()
            playersProvider = self.loadPlayersData(start)
            playerID, name = self.choosePlayer(playersProvider)
            rankingProvider = ChartPointsProvider(start, end, playerID, self.getRankingProvider())
            print('Loading ranking data...')
            self.printEnters(2)
            rankingProvider.init()
            drawer = self.getDrawer(rankingProvider, name)
            drawer.draw()

        except (InputParseException, InvalidDataException, InvalidChartDataException) as e:
            self.printErrorMessage(e)
            return
            
        
    
    def getRankingProvider(self):
        pass
    
    def getDrawer(self, provider, name):
        pass

    def chooseRankingSeasons(self):
        try:
            print('Enter start of seasons range (2013 - 2017): ')
            self.printEnters(2)
            start = int(input())
            self.printEnters(1)

            if not self.validateSeason(start):
                raise InputParseException('Start season out of range')

            print('Enter end of seasons range (2013 - 2017): ')
            self.printEnters(2)
            end = int(input())
            self.printEnters(1)

            if not self.validateSeason(end):
                raise InputParseException('End season out of range')

            if start > end:
                raise InputParseException('Invalid season range')
        
            return start, end
        
        except ValueError:
            raise InputParseException('Invalid season')

        

class RankingPositionRunner(RankingsRunner):
    def getRankingProvider(self):
        return RankingPostionProvider()

    def getDrawer(self, provider, name):
        return PositionChartDrawer(provider, name)

class RankingMoneyRunner(RankingsRunner):
    def getRankingProvider(self):
        return RankingMoneyProvider()

    def getDrawer(self, provider, name):
        return MoneyChartDrawer(provider, name)

class App:
    def __init__(self, height = 30):
        self.runner = ConsoleRunner(height)
        self.height = height

    def main(self):
        try:
            while True:
                
                print('1. Matches won in a season by a player')
                print('2. Player\'s rankings in seasons range')
                print('3. Player\'s prize money in seasons range')
                print('4. Exit')
                self.runner.printEnters(5)
                choice = input('Enter corresponding number: ')
                self.runner.printEnters(1)

                if choice == '1':
                    self.runner = MatchesRunner(self.height)
                elif choice == '2':
                    self.runner = RankingPositionRunner(self.height)
                elif choice == '3':
                    self.runner = RankingMoneyRunner(self.height)
                elif choice == '4':
                    sys.exit()
                else:
                    continue
                
                self.runner.run()

        except KeyboardInterrupt:
            pass
        finally:
            print('\n')
            print('Bye :)')
            self.runner.printEnters(3)
