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
downloadDirectory = "/media/eric/EHUPPERT700/SABR/mlb-database"

import urllib
import shutil
import xml.etree.ElementTree as ET
import datetime
import os

class Game:
	def __init__(self, year, month, day, id):
		self.localDir = downloadDirectory + "/" + str(year) + "/month_" + formattedDate(month) + "/day_" + formattedDate(day) + "/" + id
		self.baseURL = "http://gd2.mlb.com/components/game/mlb/year_" + str(year) + "/month_" + formattedDate(month) + "/day_" + formattedDate(day) + "/" + id
		try:
			os.path.exists(self.localDir)
		except OSError:
			if urllib.urlopen(self.baseURL).getcode() == 404:
				raise Exception('Cannot find the file for this game in your local directory or on the internet. Check your connection and/or if this game exists.')
		self.year = year
		self.month = month
		self.day = day
		self.id = id
		if not os.path.exists(self.localDir):
			os.makedirs(self.localDir)
		if os.path.isfile(self.localDir + "/linescore.xml"):
			self.linescoreFile = self.localDir + "/linescore.xml"
		else:
			self.linescoreFile = self.baseURL + "/linescore.xml"
		gameAttribList = ET.parse(urllib.urlopen(self.linescoreFile)).getroot().attrib
		if 'inning' in gameAttribList:
			self.innings = int(gameAttribList['inning'])
		else:
			box = urllib.urlopen(self.baseURL + "/boxscore.xml")
			boxRoot = ET.parse(box).getroot()
			for i in root.iter():
				if i.tag == 'inning_line_score':
					self.innings = int(i.attrib['inning'])	
		self.gameType = ET.parse(urllib.urlopen(self.linescoreFile)).getroot().attrib['game_type']

	def getStatus(self):
		tree = ET.parse(urllib.urlopen(self.linescoreFile))
		root = tree.getroot()
		return root.attrib['status']

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

#returns a list of all game IDs (string) for a given day
def getGames(year, month, day):
	masterScoreboardURL = "http://gd2.mlb.com/components/game/mlb/year_" + str(year) + "/month_" + formattedDate(month) + "/day_" + formattedDate(day) + "/master_scoreboard.xml"
	masterScoreboard = urllib.urlopen(masterScoreboardURL)
	if masterScoreboard.getcode() == 404:
		print "There is no master scoreboard for " + str(month) + "/" + str(day) + "/" + str(year) + " URL:" + masterScoreboardURL
	print masterScoreboardURL
	tree = ET.parse(masterScoreboard)
	root = tree.getroot()
	gameList = []
	for child in root:
		id = "gid_" + str(year) + "_" + formattedDate(month) + "_" + formattedDate(day) + "_" + child.attrib['id'][11:].replace("-", "_")
		gameList.append(Game(year, month, day, id))
	return gameList

#takes range of years as argument, downloads selected files
def getFiles(years):
	now = datetime.datetime.now()
	if 2007 in years or 2006 in years and highlights:
		print "highlights do not exist for years before 2008"
	for year in years:
		for month in range(3,12):
			for day in range (1, 32):
				if month in [4,6,9,11] and day == 31:
					continue
				if month == 2 and day in [29, 30, 31] and not (year-2000)%4 == 0:
					continue
				if month == 2 and day in [30, 31] and (year-2000)%4 == 0:
					continue
				#check to make sure you are not downloading future games
				if datetime.datetime(now.year, now.month, now.day-1) < datetime.datetime(year, month, day):
					return
				games = getGames(year, month, day)
				for game in games:
					if innings_all:
						game.getInningsAll()
					if highlights and year >= 2008:
						game.getHighlights()
					if game_events and year >= 2008:
						game.getGameEvents()
					if linescore_xml:
						game.getLinescoreXML()
					if linescore_json and year >= 2007:
						game.getLinescoreJSON()
					if box_score_xml:
						game.getBoxscoreXML()
					if box_score_json and year >= 2013:
						game.getBoxscoreJSON()
					if event_log and year >= 2007:
						game.getEventLog()
					if raw_boxscore and year >= 2011:
						game.getRawBoxscore()


						#This block of code creates the proper file structure if it does not already exist
						#if not os.path.exists("./files/"+ str(year)):
							#os.makedirs("./files/" + str(year))
						#if not os.path.exists("./files/"+ str(year) + "/month_" + formattedDate(month)):
							#os.makedirs("./files/" + str(year) + "/month_" + formattedDate(month))
						#if not os.path.exists("./files/"+ str(year) + "/month_" + formattedDate(month) + "/day_" + formattedDate(day)):
							#os.makedirs("./files/" + str(year) + "/month_" + formattedDate(month) + "/day_" + formattedDate(day))


						#This section downloads the files
						#if innings_all:
						#	print game + "/inning/inning_all.xml"
						#	(src, inst) = urllib.urlretrieve(game + "/inning/inning_all.xml", "./files/" + str(year) + "/month_" + formattedDate(month) + "/day_" + formattedDate(day) + "/" + game + "/innings_all.xml" )




#getFiles(range(2007, 2014))

#for i in gamesList:
#	for x in i:
#		if "oak" in x:
#			oakGames += 1

#print "Oakland played " + str(oakGames) + " games"

