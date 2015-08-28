####Settings####
INNINGS_ALL = True
HIGHLIGHTS = True
GAME_EVENTS = False
LINESCORE_XML = True
LINESCORE_JSON = False
BOX_SCORE_XML = False
BOX_SCORE_JSON = False
EVENT_LOG = False
GAME_LOG_XML = False
GAME_LOG_JSON = False
RAW_BOXSCORE = False
PLAYERS = True
OVERRIGHT_EXISTING_FILES = False

VERBOSE = False

import requests
from game_downloader import GameDownloader

class GameDayDownloader(object):
    """
    GameDay class looks up information about which games exist for a given day. Skips games that
    are not regular season or playoffs.
    """

    def __init__(self, date):
        """
        Fetches the scoreboard file for the day and initialize the game objects for the day.
        Takes an object of datetime.date.
        """
        self.date = date
        self.root_url = "http://gd2.mlb.com/components/game/mlb/{}".format(
            self.date.strftime("year_%Y/month_%m/day_%d"))

        scoreboard_url = self.root_url + '/master_scoreboard.json'
        response = requests.get(scoreboard_url)
        response.raise_for_status()
        games_json = response.json()['games']['game']
        game_ids = [game.gameday for game in games_json if game.game_type in
                    ['R', 'P', 'D', 'L', 'W', 'F']]
        self.games = [GameDownloader(game_id) for game_id in game_ids]


    def download_all_files(self):
        """
        Calls download on all games for this day.
        """
        for game in self.games:
            game.download_all_files()

#takes range of years as argument, downloads selected files
def getFiles(years):
    now = datetime.date.today()
    if 2007 in years or 2006 in years and highlights:
        print "highlights do not exist for years before 2008"
    for year in years:
        currentDate = datetime.date(year, 3, 23)
        endDate = min([now - datetime.timedelta(days=1), datetime.date(year, 12, 1)])
        while currentDate < endDate:
            print currentDate
            games = getGames(year, currentDate.month, currentDate.day)
            for game in games:
                if verbose:
                    print game.id
                game.getAllFiles()
            currentDate

#checks what you already have downloaded and then downloads missing files over given range
def update(start = datetime.date(2006,3,23), end = datetime.date.today()):
    now = datetime.date.today()
    currentDate = end
    while currentDate >= start: #and not hasAllFiles(getGames(currentDate.year, currentDate.month, currentDate.day)):
        print currentDate
        games = getGames(currentDate.year, currentDate.month, currentDate.day)
        for game in games:
            if verbose:
                print game
            game.getAllFiles()
        if currentDate.day == 23 and currentDate.month == 3:
            currentDate = datetime.date(currentDate.year-1, 11, 5)
        else:
            currentDate -= datetime.timedelta(days=1)

#update(end = datetime.date(2006,7,7))
