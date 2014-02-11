import os
import urllib
import xml.etree.ElementTree as ET
import shutil
dir = "/media/eric/EHUPPERT700/SABR/mlb-database"

count = 0
for root, dirs, filenames in os.walk(dir):

	for f in filenames:
		try:
			a = ET.parse(root + '/' + f)
		except:
			print root + '/' + f