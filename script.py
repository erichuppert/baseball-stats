####Settings####
innings_all = True
highlights = True
game_events = False
linescore_xml = False
linescore_json = False
box_score_xml = False
box_score_json = False
event_log = False
game_log_xml = False
game_log_json = False
raw_boxscore = False
#batters = False
#pitchers = False

#
downloadDirectory = "/media/eric/EHUPPERT700/SABR/mlb-database"

import urllib
import shutil
import xml.etree.ElementTree as ET
import datetime
import os

class Game:
	def __init__(self, id):
		self.year = int(id[4:8])
		self.month = int(id[9:11])
		self.day = int(id[12:14])
		self.id = id
		self.localDir = downloadDirectory + "/" + str(self.year) + "/month_" + formattedDate(self.month) + "/day_" + formattedDate(self.day) + "/" + id
		self.baseURL = "http://gd2.mlb.com/components/game/mlb/year_" + str(self.year) + "/month_" + formattedDate(self.month) + "/day_" + formattedDate(self.day) + "/" + id
		
		#if the game cannot be found in the download directory or on the internet, raise an exception 
		if not os.path.exists(self.localDir) and urllib.urlopen(self.baseURL).getcode() == 404:
			raise Exception('Cannot find the file for this game in your local directory or on the internet. Check your connection and/or if this game exists.')

		if not os.path.exists(self.localDir):
			os.makedirs(self.localDir)

		if os.path.isfile(self.localDir + "/linescore.xml"):
			self.linescoreFile = urllib.urlopen(self.localDir + "/linescore.xml")

		else:
			self.linescoreFile = urllib.urlopen(self.baseURL + "/linescore.xml")

		
		if self.linescoreFile.getcode() ==404:
			raise Exception('This game has no linescore file. URL ' + self.baseURL)


		gameAttribList = ET.parse(self.linescoreFile).getroot().attrib
		
		if 'inning' in gameAttribList:
			try:
				self.innings = int(gameAttribList['inning'])
			except:
				raise Exception('The inning attribute is empty URL: ' + self.baseURL)
		else:
			box = urllib.urlopen(self.baseURL + "/boxscore.xml")
			boxRoot = ET.parse(box).getroot()
			for i in boxRoot.iter():
				if i.tag == 'inning_line_score':
					self.innings = int(i.attrib['inning'])	
		self.gameType = gameAttribList['game_type'] 


	def getStatus(self):
		tree = ET.parse(urllib.urlopen(self.linescoreFile))
		root = tree.getroot()
		return root.attrib['status']

	def getAllFiles(self):
		if self.getStatus() == "Final":
			if innings_all:
				self.getInningsAll()
			if highlights and self.year >= 2008:
				self.getHighlights()
			if game_events and self.year >= 2008:
				self.getGameEvents()
			if linescore_xml:
				self.getLinescoreXML()
			if linescore_json and self.year >= 2007:
				self.getLinescoreJSON()
			if box_score_xml:
				self.getBoxscoreXML()
			if box_score_json and self.year >= 2013:
				self.getBoxscoreJSON()
			if event_log and self.year >= 2007:
				self.getEventLog()
			if raw_boxscore and self.year >= 2011:
				self.getRawBoxscore()

		else:
			print "This game is in progress or was not scored as an official game; will not get files."

	def getInningsAll(self):
		dest = self.localDir + "/innings_all.xml"
		if not os.path.isfile(dest):
			if self.year <= 2007:
				outStr = "<game>"
				for i in range(self.innings):
					inningURL = self.baseURL + "/inning/inning_" + str(i+1) + ".xml"
					data = urllib.urlopen(inningURL).read()
					outStr += data
				outStr += "</game>"
				outFile = open(dest, 'wb')
				outFile.write(outStr)
			else:
				src = self.baseURL + "/inning/inning_all.xml"
				urllib.urlretrieve(src, dest)
		else:
			print "innings_all.xml file for " + self.id + " is already downloaded"

	def getHighlights(self):
		dest = self.localDir + "/highlights.xml"
		src = self.baseURL + "/media/highlights.xml"
		if not os.path.isfile(dest):
			if self.year <= 2007:
				print "Highlights are not available for games before 2008"
			elif urllib.urlopen(src).getcode() == 404:
				print "Highlights are not available for " + self.id
			else:
				urllib.urlretrieve(src, dest)
		else:
			print "highlights.xml file for " + self.id + " is already downloaded"


	def getGameEvents(self):
		src = self.baseURL + "/game_events.xml"
		dest = self.localDir + "/game_events.xml"
		if not os.path.isfile(dest):
			if self.year == 2007:
				print "game_events.xml is not available for games before"
			elif urllib.urlopen(src).getcode() == 404:
				print "game_events.xml is not available for " + self.id
			else:
				urllib.urlretrieve(src, dest)
		else:
			"game_events.xml file for " + self.id + " is already downloaded"

	def getLinescoreXML(self):
		src = self.baseURL + "/linescore.xml"
		dest = self.localDir + "/linescore.xml"
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
		else:
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
		else:
			"boxscore.json for " + self.id + " is already downloaded"

	def getEventLog(self):
		src = self.baseURL + "/eventLog.xml"
		dest = self.localDir + "/eventLog.xml"
		if not os.path.isfile(dest):
			if self.year <= 2006:
				print "linescore.json is not available for games before 2007"
			else:
				urllib.urlretrieve(src, dest)
		else:
			"eventLog.xml for " + self.id + " is already downloaded"

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
		else:
			"rawboxscore.xml for " + self.id + " is already downloaded"

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
	for child in root:
		id = "gid_" + str(year) + "_" + formattedDate(month) + "_" + formattedDate(day) + "_" + child.attrib['id'][11:].replace("-", "_")
		print "trying to create Game instance for " + id
		
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
				print game.id
				game.getAllFiles()
			currentDate += datetime.timedelta(days=1)

#checks what you already have downloaded and then downloads missing files over given range 
def update(start = datetime.date(2006,3,23), end = datetime.date.today()):
	now = datetime.date.today()
	currentDate = end
	while not hasAllFiles(getGames(currentDate.year, currentDate.month, currentDate.day)):
		pass

#check to see if all desired for a list of games has been downloaded. Returns a boolean value.
def hasAllFiles(games):
	for game in games:
		if innings_all and not(os.path.isfile(game.localDir + "/innings_all.xml")):
			return False
		if highlights and not(os.path.isfile(game.localDir + "/highlights.xml")):
			return False
		if game_events and not(os.path.isfile(game.localDir + "/game_events.xml")):
			return False
		if linescore_xml and not(os.path.isfile(game.localDir + "/linescore.xml")):
			return False
		if linescore_json and game.year >= 2007 and not(os.path.isfile(game.localDir + "/linescore.json")):
			return False
		if box_score_xml and not(os.path.isfile(game.localDir + "/boxscore.xml")):
			return False
		if box_score_json and game.year >= 2013 and not (os.path.isfile(game.localDir + "/boxscore.json")):
			return False
		if event_log and game.year >= 2007 and not (os.path.isfile(game.localDir + "/eventLog.xml")):
			return False
		if raw_boxscore and game.year >= 2011 and not (os.path.isfile(game.localDir + "/rawboxscore.xml")):
			return False
		return True

print hasAllFiles(getGames(2010,6,8))

#print Game("gid_2010_06_08_flomlb_phimlb_1")

#getFiles(range(2012, 2014))



