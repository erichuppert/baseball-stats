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

VERBOSE = False

DOWNLOAD_DIRECTORY = "/media/eric/EHUPPERT700/SABR/mlb-database"
MLB_URL = "http://gd2.mlb.com/components/game/mlb"

import urllib
import xml.etree.ElementTree as ET
import datetime
import contextlib
import os
import json
import requests

class Game(object):
    """
    Game instance represents a single MLB game.
    """
    def __init__(self, mlb_game_id):
        """
        id has the format gid_2015_08_24_oakmlb_seamlb_1
        """
        self.mlb_game_id = mlb_game_id
        self.year = int(id[4:8])
        self.month = int(id[9:11])
        self.day = int(id[12:14])
        self.game_number = int(id[-1])

        if datetime.datetime.now() < datetime.datetime(self.year, self.month, self.day):
            raise Exception('Date of given game (' + id + ') is after current date')

        uri_suffix = "year_{}/month_{}/day_{}/{}".format(
            self.year, formattedDate(self.month), formattedDate(self.day), mlb_game_id
        )
        self.local_dir = "{}/{}/month".format(DOWNLOAD_DIRECTORY, uri_suffix)
        self.base_url = "{}/{}".format(MLB_URL, uri_suffix)

        linescore_response = requests.get(self.base_url + '/linescore.json')
        if linescore_response.status_code == 404:
            raise Exception('Game {} does not exist.'.format(mlb_game_id))
        if linescore_response.status_code != 200:
            raise Exception('Got response code of {} for game {}'.format(
                linescore_response.status_code, mlb_game_id))

        linescore = linescore_response.json()
        try:
            self.innings = int(linescore['data']['game']['inning'])
        except (KeyError, ValueError):
            raise Exception('cannot parse information from linescore file for game {}'
                            .format(mlb_game_id))

        game_type = linescore['data']['game']['game_type']
        # ensure that we are not getting a spring training or exhibition game
        if game_type not in ['R', 'P', 'D', 'L', 'W', 'F']:
            raise Exception('Game {} is not a regular season game'.format(mlb_game_id))

        if not os.path.exists(self.local_dir):
            os.makedirs(self.local_dir)



    def getStatus(self):
        f = urllib.urlopen(self.linescore_file)
        tree = ET.parse(f)
        root = tree.getroot()
        f.close()
        return root.attrib["status"]

    def getAllFiles(self):
        if INNINGS_ALL:
            self.getInningsAll()
        if HIGHLIGHTS and self.year >= 2008:
            self.getHighlights()
        if GAME_EVENTS and self.year >= 2008:
            self.getGameEvents()
        if LINESCORE_XML:
            self.getLinescoreXML()
        if LINESCORE_JSON and self.year >= 2007:
            self.getLinescoreJSON()
        if BOX_SCORE_XML:
            self.getBoxscoreXML()
        if BOX_SCORE_JSON and self.year >= 2013:
            self.getBoxscoreJSON()
        if EVENT_LOG and self.year >= 2007:
            self.getEventLog()
        if RAW_BOXSCORE and self.year >= 2011:
            self.getRawBoxscore()
        if PLAYERS:
            self.getPlayers()


    def getInningsAll(self):
        dest = self.local_dir + "/innings_all.xml"
        if not os.path.isfile(dest):
            if self.year <= 2007:
                outStr = "<game>"
                for i in range(self.innings):
                    inningURL = self.baseURL + "/inning/inning_" + str(i+1) + ".xml"
                    data = urllib.urlopen(inningURL).read()
                    outStr += data
                outStr += "</game>"
                with open(dest, 'wb') as outFile:
                    outFile.write(outStr)
            else:
                src = self.baseURL + "/inning/inning_all.xml"
                urllib.urlretrieve(src, dest)
        elif verbose:
            print "innings_all.xml file for " + self.id + " is already downloaded"

    def getHighlights(self):
        dest = self.local_dir + "/highlights.xml"
        src = self.baseURL + "/media/highlights.xml"
        if not os.path.isfile(dest):
            if self.year <= 2007:
                return
            elif urllib.urlopen(src).getcode() == 404:
                print "Highlights are not available for " + self.id
            else:
                urllib.urlretrieve(src, dest)
        elif verbose:
                print "highlights.xml file for " + self.id + " is already downloaded"


    def getGameEvents(self):
        src = self.baseURL + "/game_events.xml"
        dest = self.local_dir + "/game_events.xml"
        if not os.path.isfile(dest):
            if self.year == 2007:
                print "game_events.xml is not available for games before"
            elif urllib.urlopen(src).getcode() == 404:
                print "game_events.xml is not available for " + self.id
            else:
                urllib.urlretrieve(src, dest)
        elif verbose:
            "game_events.xml file for " + self.id + " is already downloaded"

    def getLinescoreXML(self):
        src = self.baseURL + "/linescore.xml"
        dest = self.local_dir + "/linescore.xml"
        if os.path.isfile(dest):
            "linescore.xml for " + self.id + " is already downloaded"
        elif urllib.urlopen(src).getcode() == 404:
            print "linescore.xml is not available for " + self.id
        else:
            urllib.urlretrieve(src, dest)

    def getPlayers(self):
            src = self.baseURL + "/players.xml"
            dest = self.localDir + "/players.xml"
            if os.path.isfile(dest):
                "linescore.xml for " + self.id + " is already downloaded"
            elif urllib.urlopen(src).getcode() == 404:
                print "linescore.xml is not available for " + self.id
            else:
                urllib.urlretrieve(src, dest)


    def getLinescoreJSON(self):
        src = self.baseURL + "/linescore.json"
        dest = self.localDir + "/linescore.json"
        if not os.path.isfile(dest):
            if self.year <= 2007:
                print "linescore.json is not available for games before 2008"
            elif urllib.urlopen(src).getcode() == 404:
                print "linescore.json is not available for " + self.id
            else:
                urllib.urlretrieve(src, dest)
        elif verbose:
            "linescore.json for " + self.id + " is already downloaded"

    def getBoxscoreXML(self):
        src = self.baseURL + "/boxscore.xml"
        dest = self.localDir + "/boxscore.xml"
        if os.path.isfile(dest):
            "boxscore.xml for " + self.id + " is already downloaded"
        elif urllib.urlopen(src).getcode() == 404:
            print "boxscore.xml is not available for " + self.id
        else:
            urllib.urlretrieve(src, dest)

    def getBoxscoreJSON(self):
        src = self.baseURL + "/boxscore.json"
        dest = self.localDir + "/boxscore.json"
        if not os.path.isfile(dest):
            if self.year <= 2011:
                print "linescore.json is not available for games before 2012"
            else:
                urllib.urlretrieve(src, dest)
        elif verbose:
            "boxscore.json for " + self.id + " is already downloaded"

    def getEventLog(self):
        src = self.baseURL + "/eventLog.xml"
        dest = self.localDir + "/eventLog.xml"
        if not os.path.isfile(dest):
            if self.year <= 2006:
                print "linescore.json is not available for games before 2007"
            else:
                urllib.urlretrieve(src, dest)
        elif verbose:
            print "eventLog.xml for " + self.id + " is already downloaded"

    def getRawBoxscore(self):
        src = self.baseURL + "/rawboxscore.xml"
        dest = self.localDir + "/rawboxscore.xml"
        if not os.path.isfile(dest):
            if self.year <= 2011:
                print "rawboxscore.xml is not available for games before 2012"
            elif urllib.urlopen(src).getcode() == 404:
                print "rawboxscore.xml is not available for " + self.id
            else:
                urllib.urlretrieve(src, dest)
        elif verbose:
            print "rawboxscore.xml for " + self.id + " is already downloaded"

#returns a properly formatted string for date (adds a leading zero to single digit numbers)
def formattedDate(number):
    if number < 10:
        return "0" + str(number)
    else:
        return str(number)

#returns a list of all game objects for a given day
def getGames(year, month, day):
    masterScoreboardURL = "http://gd2.mlb.com/components/game/mlb/year_" + str(year) + "/month_" + formattedDate(month) + "/day_" + formattedDate(day) + "/master_scoreboard.xml"
    masterScoreboard = urllib.urlopen(masterScoreboardURL)
    if masterScoreboard.getcode() == 404:
        print "There is no master scoreboard for " + str(month) + "/" + str(day) + "/" + str(year) + " URL: " + masterScoreboardURL
        print masterScoreboardURL
        return []
    tree = ET.parse(masterScoreboard)
    root = tree.getroot()
    gameList = []
    masterScoreboard.close()
    for child in root:
        id = "gid_" + str(year) + "_" + formattedDate(month) + "_" + formattedDate(day) + "_" + child.attrib['id'][11:].replace("-", "_")

        try:
            gameList.append(Game(id))

        except Exception as exc:
            print exc
            continue
    return gameList

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

#check to see if all desired for a list of games has been downloaded. Returns a boolean value.
def hasAllFiles(games):
    for game in games:
        if INNINGS_ALL and not(os.path.isfile(game.localDir + "/innings_all.xml")):
            return False
        if HIGHLIGHTS and not(os.path.isfile(game.localDir + "/highlights.xml")):
            return False
        if GAME_EVENTS and not(os.path.isfile(game.localDir + "/game_events.xml")):
            return False
        if LINESCORE_XML and not(os.path.isfile(game.localDir + "/linescore.xml")):
            return False
        if LINESCORE_JSON and game.year >= 2007 and not(os.path.isfile(game.localDir + "/linescore.json")):
            return False
        if BOX_SCORE_XML and not(os.path.isfile(game.localDir + "/boxscore.xml")):
            return False
        if BOX_SCORE_JSON and game.year >= 2013 and not (os.path.isfile(game.localDir + "/boxscore.json")):
            return False
        if EVENT_LOG and game.year >= 2007 and not (os.path.isfile(game.localDir + "/eventLog.xml")):
            return False
        if RAW_BOXSCORE and game.year >= 2011 and not (os.path.isfile(game.localDir + "/rawboxscore.xml")):
            return False
        if players AND not (os.path.isfile(game.localDir + "/players.xml")):
            return False
        return True


#update(end = datetime.date(2006,7,7))
