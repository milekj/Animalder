from exceptions import *

import urllib.request
import urllib.error
import json

class DataDownloader:
    def download(url, timeout):
        try:
            req = urllib.request.urlopen(url, timeout = timeout)
            playersJSON = req.read()
            return json.loads(playersJSON)

        except ValueError:
            raise DataDownloadException('Invalid URL')
        except urllib.error.URLError:
            raise DataDownloadException('Cannot retrieve data from server')
        except json.JSONDecodeError:
            raise DataDownloadException('Downloaded data is invalid')
        

class PlayersDataProvider:
    urlBase = 'http://api.snooker.org/?t=10&st=p'

    def __init__(self, season):
        self.season = season
        self.urlComplete = PlayersDataProvider.urlBase + '&s=' + str(season)
        self.playersData = []
    
    def init(self):
        try:            
            self.playersData = DataDownloader.download(self.urlComplete, 10)
        except DataDownloadException as e:
            raise InvalidDataException('Players data is invalid. Cause: ' + str(e))
        
        self.validate()
        
        
    def getPlayersNames(self):
        self.validate()

        return [ {'id':p['ID'], 'fullName':p['FirstName'] + ' ' + p['LastName']} for p in self.playersData]
    
    def validate(self):
        if not self.playersData:
            raise InvalidDataException('Players data is empty')

class PlayerFinder:
    def __init__(self, players):
        self.players = players
    
    def getMatchingPlayers(self, text):
        return list(filter(lambda p: p['fullName'].upper().find(text.upper()) != -1, self.players.getPlayersNames()))
        
class MatchesDataProvider:
    urlBase = 'http://api.snooker.org/?t=8'

    def __init__(self, id, season, name):
        self.id = id
        self.season = season
        self.urlComplete = self.urlBase + '&p=' + str(id) + '&s=' + str(season)
        self.name = name
        self.matchesData = []
    
    def init(self):
        try:
            self.matchesData = DataDownloader.download(self.urlComplete, 10)
        except DataDownloadException as e:
            raise InvalidDataException('Matches data is invalid. Cause: ' + str(e))
        
        self.validate()

    def getPlayed(self):
        self.validate()
        return len(self.matchesData)
    
    def getWon(self):
        self.validate()
        return len(list(filter(lambda y: y == self.id, map(lambda x: x['WinnerID'], self.matchesData))))
    
    def getName(self):
        return self.name

    def getSeason(self):
        return self.season
    
    def validate(self):
        if not self.matchesData:
            raise InvalidDataException('Matches data is empty')

class PlayerRankingDataProvider:
    urlBase = 'http://api.snooker.org/?rt=MoneyRankings'

    def __init__(self, season, id):
        self.urlComplete = self.urlBase + '&s=' + str(season)
        self.id = id
        self.playerRankingData = []

    def init(self):
        try:
            rankingData = DataDownloader.download(self.urlComplete, 10)
            self.playerRankingData = list(filter(lambda x: x['PlayerID'] == self.id, rankingData))

        except DataDownloadException as e:
            raise InvalidDataException('Ranking data is invalid. Cause: ' + str(e))
        
        if not self.playerRankingData:
            raise InvalidDataException('Ranking data is empty')

    def getPlayerPosition(self):
        if self.playerRankingData:
            return self.playerRankingData[0]['Position']
        else:
            return -1
    
    def getPlayerMoney(self):
        if self.playerRankingData:
            return self.playerRankingData[0]['Sum']
        else:
            return -1        

class RankingValueProvider:
    def getValue(self):
        pass

class RankingPostionProvider(RankingValueProvider):
    def getValue(self, provider):
        return provider.getPlayerPosition()

class RankingMoneyProvider(RankingValueProvider):
    def getValue(self, provider):
        return provider.getPlayerMoney()

class ChartPointsProvider:
    def __init__(self, start, end, id, provider):
        self.start = start
        self.end = end
        self.id = id
        self.valueProvider = provider
        self.x = []
        self.y = []
    
    def init(self):
        if self.start > self.end:
            raise InvalidDataException('Chart points are empty, beacause season range is invalid')

        s = self.start
        while s <= self.end:
            rankingProvider = PlayerRankingDataProvider(s, self.id)
            rankingProvider.init()
            rank = self.valueProvider.getValue(rankingProvider)
            if rank != -1:                
                self.x.append(s)
                self.y.append(rank)
            s += 1
        
        self.validate()

    def getRangeRanking(self):
        self.validate()
        return self.x, self.y
    
    def validate(self):
        if not self.x:
            raise InvalidDataException('Chart points are empty')
