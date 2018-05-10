import unittest
from providers import *
from exceptions import *
from charts import *

class TestDownload(unittest.TestCase):
    def testInvalidURL(self):
        with self.assertRaises(DataDownloadException):
            DataDownloader.download('invalidURL', 10)
    
    def testJSONDownload(self):
        expected = [{"ID": 1,"Type": 1,"FirstName": "Mark","MiddleName": "J","LastName": "Williams",
        "TeamName": "","TeamNumber": 0,"TeamSeason": 0,"ShortName": "M J Williams","Nationality": "Wales",
        "Sex": "M","BioPage": "http:\u002F\u002Fsnooker.org\u002Fplr\u002Fbio\u002Fmwilliams.shtml",
        "Born": "1975-03-21","Twitter": "markwil147","SurnameFirst": False,"License": "","Club": "",
        "URL": "","Photo": "http:\u002F\u002Fsnooker.org\u002Fimg\u002Fplayers\u002FMarkWilliams.png",
        "PhotoSource": "","FirstSeasonAsPro": 1992,"LastSeasonAsPro": 0,"Info": ""}]
        self.assertEqual(DataDownloader.download('http://api.snooker.org/?p=1', 10), expected)

class TestPlayersDataProvider(unittest.TestCase):
    def testContains(self):
        provider = PlayersDataProvider(2015)
        provider.init()
        players = provider.getPlayersNames()
        self.assertTrue({'id': 1, 'fullName': 'Mark Williams'} in players)
    
    def testEmpty(self):
        provider = PlayersDataProvider(2000)
        with self.assertRaises(InvalidDataException):
            provider.init()
    
    def testWithoutInit(self):
        provider = PlayersDataProvider(2015)
        with self.assertRaises(InvalidDataException):
            provider.getPlayersNames()

    
class TestPlayerFinder(unittest.TestCase):
    provider = PlayersDataProvider(2015)
    provider.init()
    finder = PlayerFinder(provider)

    def testFound(self):
        players = TestPlayerFinder.finder.getMatchingPlayers('Will')
        self.assertTrue({'id': 1, 'fullName': 'Mark Williams'} in players)
    
    def testNotFound(self):
        players = TestPlayerFinder.finder.getMatchingPlayers('noSuchName')
        self.assertFalse({'id': 1, 'fullName': 'Mark Williams'} in players)
    
    def emptyString(self):
        players = TestPlayerFinder.finder.getMatchingPlayers('')
        self.assertFalse(players)


class TestMatchesDataProvider(unittest.TestCase):
    provider = MatchesDataProvider(1, 2015, 'Mark Williams')
    provider.init()

    def testPlayed(self):    
        self.assertEqual(TestMatchesDataProvider.provider.getPlayed(), 97)

    def testWon(self):
        self.assertEqual(TestMatchesDataProvider.provider.getWon(), 60)
    
    def testName(self):
        self.assertEqual(TestMatchesDataProvider.provider.getName(), 'Mark Williams')
    
    def testSeason(self):
        self.assertEqual(TestMatchesDataProvider.provider.getSeason(), 2015)
    
    def testInvalidID(self):
        invalidProvider = MatchesDataProvider(-20, 2015, 'Ex Example')
        with self.assertRaises(InvalidDataException):
            invalidProvider.init()
    
    def testInvalidSeason(self):
        invalidProvider = MatchesDataProvider(1, 0, 'Ex Example')
        with self.assertRaises(InvalidDataException):
            invalidProvider.init()
    
    def testWithoutInit(self):
        provider = MatchesDataProvider(1, 2015, 'Mark Williams')
        with self.assertRaises(InvalidDataException):
            provider.getPlayed()

class TestPlayerRankingDataProvider(unittest.TestCase):
    provider = PlayerRankingDataProvider(2015, 1)
    provider.init()

    def testPosition(self):
        self.assertEqual(13, TestPlayerRankingDataProvider.provider.getPlayerPosition())

    def testMoney(self):
        self.assertEqual(237375, TestPlayerRankingDataProvider.provider.getPlayerMoney())
    
    def testInvalidSeason(self):
        with self.assertRaises(InvalidDataException):
            invalidProvider = PlayerRankingDataProvider(0, 1)
            invalidProvider.init()
    
    def testInvalidID(self):
        with self.assertRaises(InvalidDataException):
            invalidProvider = PlayerRankingDataProvider(2015, -300)
            invalidProvider.init()
    
    def testNoPlayerInASeason(self):
        provider = PlayerRankingDataProvider(2017, 582)
        self.assertEqual(-1, provider.getPlayerPosition())
        self.assertEqual(-1, provider.getPlayerMoney())

class TestChartPointsProvider(unittest.TestCase):
    def testWithPositionProvider(self):
        provider = ChartPointsProvider(2015, 2016, 1, RankingPostionProvider())
        provider.init()
        self.assertEqual(([2015, 2016], [13, 15]), provider.getRangeRanking())
    
    def testWithMoneyProvider(self):
        provider = ChartPointsProvider(2015, 2016, 1, RankingMoneyProvider())
        provider.init()
        self.assertEqual(([2015, 2016], [237375, 211975]), provider.getRangeRanking())
    
    def testWithoutInit(self):
        provider = ChartPointsProvider(2015, 2016, 1, RankingPostionProvider())
        with self.assertRaises(InvalidDataException):
            provider.getRangeRanking()
    
    def testInvalidRange(self):
        provider = ChartPointsProvider(2017, 2015, 1, RankingPostionProvider())
        with self.assertRaises(InvalidDataException):
            provider.init()
    
    def testInvalidSeasons(self):
        provider = ChartPointsProvider(0, 6, 1, RankingPostionProvider())
        with self.assertRaises(InvalidDataException):
            provider.init()

class TestChartDrawers(unittest.TestCase):
    def testInvalidProviderForMatches(self):
        provider = MatchesDataProvider(1, 0, 'Ex Example')
        drawer = MatchesChartDrawer(provider)
        with self.assertRaises(InvalidChartDataException):
            drawer.draw()
    
    def testInvalidProviderForRankings(self):
        provider = ChartPointsProvider(0, 10, 1, RankingPostionProvider())
        drawer = PositionChartDrawer(provider, 'Ex Example')
        with self.assertRaises(InvalidChartDataException):
            drawer.draw()
    
if __name__ == '__main__':
    unittest.main()