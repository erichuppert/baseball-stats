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

#returns a properly formatted string for date (adds a leading zero to single digit numbers)
def formattedDate(number):
	if number < 10:
		return "0" + str(number)
	else:
		return str(number)

#returns a list of the URLs that point to files pertaining to all the games in a day
def getGamesURL(year, month, day):
	url = "http://gd2.mlb.com/components/game/mlb/year_" + str(year) + "/month_" +formattedDate(month) + "/day_" + formattedDate(day) + "/master_scoreboard.xml"
	(src, inst) = urllib.urlretrieve(url)
	#dest = "/home/eric/Projects/baseball_database/files"
	tree = ET.parse(src)
	root = tree.getroot()
	baseURLs = []
	for child in root:
		baseURLs.append("http://gd2.mlb.com/components/game/mlb/year_" + str(year) + "/month_" +formattedDate(month) + "/day_" + formattedDate(day) + "/gid_" +str(year) + '_' + formattedDate(month) + '_' + formattedDate(day) + '_' + child.attrib['id'][11:].replace("-", "_"))
	return baseURLs


#takes range of years as argument, downloads selected files
def getFiles(years):
	now = datetime.datetime.now()
	for year in years:
		for month in range(7,12):
			for day in range (1, 32):
				if month in [4,6,9,11] and day == 31:
					continue
				#check to make sure you are not downloading future games
				if datetime.datetime(now.year, now.month, now.day-1) < datetime.datetime(year, month, day):
					return
				gameList = getGamesURL(year, month, day)
				if innings_all:
					for game in gameList:
						(src, inst) = urllib.urlretrieve(game + "/inning/inning_all.xml")
						if not os.path.exists("./files/"+ str(year)):
							os.makedirs("./files/" + str(year))
						if not os.path.exists("./files/"+ formattedDate(month)):
							os.makedirs("./file/s" + formattedDate(month))
						if not os.path.exists("./files/"+ formattedDate(day)):
							os.makedirs("./files/" + formattedDate(day))
						os.rename(src, "./files/" + str(year) + "/" + formattedDate(month) + "/" + formattedDate(day) + "/" + game + ".xml")








getFiles(range(2007, 2014))

#for i in gamesList:
#	for x in i:
#		if "oak" in x:
#			oakGames += 1

#print "Oakland played " + str(oakGames) + " games"

