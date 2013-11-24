import os
import urllib
import xml.etree.ElementTree as ET
import shutil
dir = "/media/eric/EHUPPERT700/SABR/mlb-database/2012"
broken = []
noLS = []
postponed = []
spring = []
for root, dirs, filenames in os.walk(dir):
	if len(dirs) == 0:
		#print root+'/linescore.xml'
		if os.path.isfile(root+'/linescore.xml'):
			pass
			x = urllib.urlopen(root+'/linescore.xml')
			tree = ET.parse(x)
			r = tree.getroot()
			if r.attrib['game_type'] == 'S' or r.attrib['game_type'] == 'E':
				shutil.rmtree(root)
				continue
			elif r.attrib['status'] == 'Postponed':
				shutil.rmtree(root)
				continue
				#postponed.append(root)

			x.close()
		else:
			u = "http://gd2.mlb.com/components/game/mlb/year_" + root[42:] +'/linescore.xml'
			print u
			x = urllib.urlopen(u)
			if x.getcode() == 404:
				shutil.rmtree(root)
				continue
			tree = ET.parse(x)
			r = tree.getroot()
			if r.attrib['game_type'] == 'S':
				shutil.rmtree(root)
				continue
			elif r.attrib['status'] == 'Postponed':
				shutil.rmtree(root)
				continue
				#postponed.append(root)

			else:
				noLS.append(root)
