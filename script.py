####Settings####
innings_all = True
media_files = True
game_events = False
linescore_xml = False
linescore_json = False
box_score_xml = False
box_score_json = False
event_log = False
raw_boxscore = False
#batters = False
#pitchers = False

import urllib
import shutil
import xml.etree.ElementTree as ET
import datetime
import os

class Game:
	def __init__(self, year, month, day, id):
		self.year = year
		self.month = month
		self.day = day
		self.id = id
		self.baseURL = "http://gd2.mlb.com/components/game/mlb/year_" + str(year) + "/month_" + formattedDate(month) + "/day_" + formattedDate(day) + "/" + id
		self.localDir = "./files/" + str(year) + "/month_" + formattedDate(month) + "/day_" + formattedDate(day) + "/" + id
		if not os.path.exists(self.localDir):
			os.makedirs(self.localDir)

	def getInningsAll(self):
		src = self.baseURL + "/inning/inning_all.xml"
		dest = self.localDir + "/innings_all.xml"
		urllib.urlretrieve(src, dest)

	def getMedia(self):
		src = self.baseURL + "/media/highlights.xml"
		dest = self.localDir + "/highlights.xml"
		urllib.urlretrieve(src, dest)

	def getGameEvents(self):
		src = self.baseURL + "/game_events.xml"
		dest = self.localDir + "/game_events.xml"
		urllib.urlretrieve(src, dest)

	def getLinescoreXML(self):
		src = self.baseURL + "/linescore.xml"
		dest = self.localDir + "/linescore.xml"
		urllib.urlretrieve(src, dest)

	def getLinescoreJSON(self):
		src = self.baseURL + "/linescore.json"
		dest = self.localDir + "/linescore.jspon"
		urllib.urlretrieve(src, dest)

	def getBoxscoreXML(self):
		src = self.baseURL + "/boxscore.xml"
		dest = self.localDir + "/boxscore.xml"
		urllib.urlretrieve(src, dest)

	def getBoxscoreJSON(self):
		src = self.baseURL + "/boxscore.json"
		dest = self.localDir + "/boxscore.json"
		urllib.urlretrieve(src, dest)

	def getEventLog(self):
		src = self.baseURL + "/eventLog.xml"
		dest = self.localDir + "/eventLog.xml"
		urllib.urlretrieve(src, dest)

#returns a properly formatted string for date (adds a leading zero to single digit numbers)
def formattedDate(number):
	if number < 10:
		return "0" + str(number)
	else:
		return str(number)

#returns a list of all game IDs (string) for a given day
def getGameIDs(year, month, day):
	url = "http://gd2.mlb.com/components/game/mlb/year_" + str(year) + "/month_" + formattedDate(month) + "/day_" + formattedDate(day) + "/master_scoreboard.xml"
	(src, inst) = urllib.urlretrieve(url)
	#dest = "/home/eric/Projects/baseball_database/files"
	tree = ET.parse(src)
	root = tree.getroot()
	idList = []
	for child in root:
		idList.append(child.attrib['id'][11:].replace("-", "_"))
	return idList

#Downloads the "innings_all.xml" file and places it in the proper game directory
def getInningsAll(year, month, day, gameID):
	src = "http://gd2.mlb.com/components/game/mlb/year_" + str(year) + "/month_" + formattedDate(month) + "/day_" + formattedDate(day) + "/" + gameID
	dest = "./files/" + str(year) + "/month_" + formattedDate(month) + "/day_" + formattedDate(day) + "/" + gameID + "/innings_all.xml"
	if not os.path.exists("./files/"+ str(year) + "/month_" + formattedDate(month) + "/day_" + formattedDate(day) + "/" + gameID):
		os.makedirs("./files/" + str(year) + "/month_" + formattedDate(month) + "/day_" + formattedDate(day) + "/" + gameID)
	urllib.urlretrieve(src, dest)

#given a game date and ID, returns a boolean describing if a game is complete
def isDone(year, month, day, gameID):
        pass

#given a game date and ID, returns a string describing the type of game (spring training, regular season, playoffs, or other)
def gameType():
        pass
        

#takes range of years as argument, downloads selected files
def getFiles(years):
	now = datetime.datetime.now()
	for year in years:
		for month in range(4,12):
			for day in range (1, 32):
				if month in [4,6,9,11] and day == 31:
					continue
				#check to make sure you are not downloading future games
				if datetime.datetime(now.year, now.month, now.day-1) < datetime.datetime(year, month, day):
					return
				gameIDs = getGameIDs(year, month, day)
				if innings_all:
					for gameID in gameIDs:
						getInningsAll(year, month, day, gameID)

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

