import os
import xml.etree.ElementTree as ET
import MySQLdb

db = MySQLdb.connect("localhost", "baseball", "baseball1", "baseball")
cursor = db.cursor()
directory = "" #define this
for root, dirs, filenames in os.walk(directory):
	if not (len(dirs) == 0 and len(filenames) == 2):
		continue
	print root
	highlightsFilePath = root + "highlights.xml"
	highlightXmlRoot =  ET.parse(highlightsFilePath).getroot()
	gameHighlights = highlightXmlRoot.getchildren()
	for highlight in gameHighlights:
		pass
