import os
import urllib
import xml.etree.ElementTree as ET
import shutil
dir = "/media/eric/EHUPPERT700/SABR/mlb-database/2011"
teams =  ['sln', 'was','det', 'cin', 'nyn', 'tba', 'bos', 'cha', 'min',
'kca', 'hou', 'sln', 'ari', 'lan', 'sea', 'sfn', 'chn', 'cle', 'mil', 'pit',
'sdn', 'tor', 'ana', 'bal', 'nya', 'tex', 'col', 'phi', 'flo', 'oak', 'atl', 
]

counts = {}

for t in teams:
	counts[t] = 0

for root, dirs, filenames in os.walk(dir):
	if len(dirs) == 0:
		f = urllib.urlopen(root+'/linescore.xml')
		t = ET.parse(f)
		r = t.getroot()
		a = r.attrib
		if not (a['status'] == 'Final' or a['status'] == 'Completed Early'):
			print a['status']
			print root
		if a['game_type'] == 'R' and (a['status'] == 'Final' or a['status'] == 'Completed Early'):
				counts[a['away_code']] += 1
				counts[a['home_code']] += 1


for i in counts.iterkeys():
	if counts[i] != 162:
		print i