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
downloadDirectory = "/home/eric/Projects/baseball_database/files"

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
			pass
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
		self.innings = int(ET.parse(urllib.urlopen(self.linescoreFile)).getroot().attrib['inning'])
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
		if urllib.urlopen(src).getcode() == 404:
			print "linescore.xml is not available for " + self.id
		elif not os.path.isfile(dest):
			urllib.urlretrieve(src, dest)
		else:
			"linescore.xml for " + self.id + " is already downloaded"

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
		if urllib.urlopen(src).getcode() == 404:
			print "boxscore.xml is not available for " + self.id
		elif not os.path.isfile(dest):
			urllib.urlretrieve(src, dest)
		else:
			"boxscore.xml for " + self.id + " is already downloaded"

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
	tree = ET.parse(urllib.urlopen(masterScoreboardURL))
	root = tree.getroot()
	gameList = []
	for child in root:
		id = "gid_" + str(year) + "_" + formattedDate(month) + "_" + formattedDate(day) + "_" + child.attrib['id'][11:].replace("-", "_")
		print id
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
				#check to make sure you are not downloading future games
				if datetime.datetime(now.year, now.month, now.day-1) < datetime.datetime(year, month, day):
					return
				games = getGames(year, month, day)
				for game in games:
					if innings_all:
						game.getInningsAll()
					if highlights:
						game.getHighlights()
				#if game_events:
				#if linescore_xml:
				#if linescore_json:
				#if box_score_xml:
				#if box_score_json:
				#if event_log:
				#if game_log_xml:
				#if game_log_json:
				#if raw_boxscore:


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

