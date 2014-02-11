import os
from download import Game
import urllib
import xml.etree.ElementTree as ET

def fix():
	badGames = open('wrong.txt')
	for line in badGames:
		if os.path.isfile(line[:-1]):
			#this is gid+"/inning.xml"
			os.remove(line[:-1])
			try:
				g = Game(line[63:93])
			except:
				continue
			g.getLinescoreXML()
			try:
				ET.parse(line[:-1])
				print 'Fixed ' + line[63:93]
			except:
				print line[63:93] + " still sucks"



