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

DOWNLOAD_DIRECTORY = "/media/eric/EHUPPERT700/SABR/mlb-database"
MLB_URL = "http://gd2.mlb.com/components/game/mlb"

import urllib
import xml.etree.ElementTree as ET
from datetime import date
import os
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
        self.game_number = int(id[-1])

        year = int(id[4:8])
        month = int(id[9:11])
        day = int(id[12:14])
        self.date = date(year, month, day)

        # TODO: handle timezones more gracefully
        if date.today() < self.date:
            raise Exception('Date of given game (' + mlb_game_id + ') is after current date')

        uri_suffix = "{}/{}".format(self.date.strftime("year_%Y/month_%m/day_%d"), mlb_game_id)
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

    def get_all_files(self):
        """
        Checks settings and downloads all the files that are needed
        """
        if INNINGS_ALL:
            self.download_innings_all_file()
        if HIGHLIGHTS:
            self.download_highlights_file()
        if GAME_EVENTS:
            self.download_game_events_file()
        if LINESCORE_XML:
            self.download_linescore_xml()
        if LINESCORE_JSON:
            self.download_linescore_json()
        if BOX_SCORE_XML:
            self.download_boxscore_xml()
        if BOX_SCORE_JSON:
            self.download_boxscore_json()
        if RAW_BOXSCORE:
            self.download_raw_boxscore_file()
        if PLAYERS:
            self.download_players_file()

    def download_file(self, file_url, local_file_path, minimum_year=0):
        """
        given a the url of a file and a location to download the file to, downloads the file.
        Optionally takes a minimum_year value, which will skip the download if self.year is
        less than minimum_year. This optional value should be used when some file type was not
        in existance for some year
        """
        if self.date.year < minimum_year:
            return
        file_exists = os.path.isfile(local_file_path)
        if file_exists or not OVERRIGHT_EXISTING_FILES:
            return

        if not file_exists or OVERRIGHT_EXISTING_FILES:
            response = requests.get(file_url)
            response.raise_for_status()
            with open(local_file_path, 'wb') as local_file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        local_file.write(chunk)
                        local_file.flush()

    def download_innings_all_file(self):
        """
        Downloads the 'innings_all' file, which contains pitch by pitch data, including PitchF/X
        information. Before the year of 2008, these files don't exist for the entire game, but for
        individual innings. This method handles 2007 gracefully by concatenating the files for each
        inning so that the downloaded file always has the same format
        """
        dest = self.local_dir + "/innings_all.xml"
        if not os.path.isfile(dest):
            if self.date.year < 2008:
                full_xml = "<game>"
                for i in range(self.innings):
                    inning_url = "{}/inning/innging{}.xml".format(self.base_url, str(i+1))
                    response = requests.get(inning_url)
                    response.raise_for_status()
                    full_xml += response.text
                full_xml += "</game>"
                with open(dest, 'wb') as output_file:
                    output_file.write(full_xml)
            else:
                src = self.base_url + "/inning/inning_all.xml"
                self.download_file(src, dest)

    def download_highlights_file(self):
        """
        Downloads the highlights file for the game, which contains information about video
        highlights for a game.
        """
        dest = self.local_dir + "/highlights.xml"
        src = self.base_url + "/media/highlights.xml"
        self.download_file(src, dest, minimum_year=2008)


    def download_game_events_file(self):
        """
        Downloads the game events file, which contains play by play information about the game
        """
        src = self.base_url + "/game_events.xml"
        dest = self.local_dir + "/game_events.xml"
        self.download_file(src, dest, minimum_year=2008)

    def download_linescore_xml(self):
        """
        Downloads the linescore file for a game, which contains the basic overview of the game's
        stats. Uses xml format
        """
        src = self.base_url + "/linescore.xml"
        dest = self.local_dir + "/linescore.xml"
        self.download_file(src, dest)

    def download_players_file(self):
        """
        downloads the players file for a given game, which gives a snapshot of the
        """
        src = self.base_url + "/players.xml"
        dest = self.local_dir + "/players.xml"
        self.download_file(src, dest)


    def download_linescore_json(self):
        """
        Downloads the linescore file for a game, which contains the basic overview of the game's
        stats. Uses json format
        """
        src = self.base_url + "/linescore.json"
        dest = self.local_dir + "/linescore.json"
        self.download_file(src, dest, minimum_year=2008)

    def download_boxscore_xml(self):
        """
        Downloads the boxscore file in xml format
        """
        src = self.base_url + "/boxscore.xml"
        dest = self.local_dir + "/boxscore.xml"
        self.download_file(src, dest)

    def download_boxscore_json(self):
        """
        Downloads the boxscore file in xml format
        """
        src = self.base_url + "/boxscore.json"
        dest = self.local_dir + "/boxscore.json"
        self.download_file(src, dest)

    def download_raw_boxscore_file(self):
        """
        Downloads the raw boxscore file
        """
        src = self.base_url + "/rawboxscore.xml"
        dest = self.local_dir + "/rawboxscore.xml"
        self.download_file(src, dest, minimum_year=2012)


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

#update(end = datetime.date(2006,7,7))
