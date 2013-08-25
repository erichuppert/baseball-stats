import urllib
import shutil
import xml.etree.ElementTree as ET
import datetime

#returns a properly formatted string for date (adds a leading zero to single digit numbers)
def formattedDate(number):
	if number < 10:
		return "0" + str(number)
	else:
		return str(number)

#returns a list of strings of a days games in the form 
def getGamesURL(year, month, day):
	url = "http://gd2.mlb.com/components/game/mlb/year_" + str(year) + "/month_" +formattedDate(month) + "/day_" + formattedDate(day) + "/master_scoreboard.xml"
	(src, inst) = urllib.urlretrieve(url)
	#dest = "/home/eric/Projects/baseball_database/files"
	tree = ET.parse(src)
	root = tree.getroot()
	games = []
	for child in root:
		games.append("http://gd2.mlb.com/components/game/mlb/year_" + str(year) + "/month_" +formattedDate(month) + "/day_" + formattedDate(day) + "/gid_" +str(year) + '_' + formattedDate(month) + '_' + formattedDate(day) + '_' + child.attrib['id'][11:].replace("-", "_") + "/inning/inning_all.xml")
	return games



def getFiles():
	now = datetime.datetime.now()
	for year in range(2013,2014):
		for month in range(7,12):
			for day in range (1, 32):
				if month in [4,6,9,11] and day == 31:
					continue
				#check to make sure you are not downloading future games
				if datetime.datetime(now.year, now.month, now.day-1) < datetime.datetime(year, month, day):
					return
				gameList = getGamesURL(year, month, day)
				print str(gameList)


getFiles()

#for i in gamesList:
#	for x in i:
#		if "oak" in x:
#			oakGames += 1

#print "Oakland played " + str(oakGames) + " games"

