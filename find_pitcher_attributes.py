import MySQLdb
import numpy
from sklearn.cluster import MeanShift, estimate_bandwidth

#initialize db connection
db = MySQLdb.connect("localhost", "baseball", "baseball1", "baseball")
cursor = db.cursor()


pitchTypes = {
	# fastballs
	'FF' : ['FA', 'FF'],
	'FT' : ['FT'],
	'FC' : ['FC'],
	'FS' : ['FS', 'SI'],
	# offspeed
	'SL' : ['SL'],
	'CH' : ['CH'],
	'CB' : ['CB', 'CU' 'KC'],
	'KN' : ['KN'],
	'EP' : ['EP'],
	'SC' : ['SC']
}


#############  retrieve data from database  #############

# get all pitcher IDs
selectAllPitchersSQL = """SELECT id, throws FROM player
WHERE throws IS NOT NULL"""
cursor.execute(selectAllPitchersSQL)
pitchers=cursor.fetchall()
numPitchers = len(pitchers)
statLabels = ['start_speed', 'end_speed', 'pfx_x', 'pfx_z', 'vx0', 'vy0', 'vz0', 
 	'ax', 'ay', 'az', 'break_y', 'break_angle']


# createSQL = """CREATE table pitcher_clusters (
# 		id int,
# 		throws char(1),
# 	"""
# allLabels = []
# pt = pitchTypes.keys()
# for pitch in pt:
# 	allLabels.append(pitch + "_usage float") 
# 	allLabels += [pitch+ "_" + label + " float" for label in statLabels]
# createSQL += ", ".join(allLabels)
# createSQL += ")"
# print createSQL


for i in xrange(len(pitchers)):
	print "%i/%i pitchers fetched" % (i, numPitchers)
	pitcherID, pitcherThrows = pitchers[i];
	insertLabelsSQL = "id, throws"
	insertValuesSQL = "%i, '%s'" % (pitcherID, pitcherThrows)
	totalPitchCountSQL = """SELECT COUNT(pitch.id) FROM pitch JOIN atbat ON atbat.id = pitch.atbat_id
			WHERE atbat.pitcher=%i""" % pitcherID
	cursor.execute(totalPitchCountSQL)
	totalPitchCount = cursor.fetchall()[0][0]
	for pitchType in pitchTypes.keys():
		allPitchLabels = ["'%s'" % name for name in pitchTypes[pitchType]]
		pitchTypeCountSQL = """SELECT COUNT(pitch.id) FROM pitch JOIN atbat ON atbat.id = pitch.atbat_id
			WHERE atbat.pitcher = %i AND pitch_type IN (%s)""" % (pitcherID, ", ".join(allPitchLabels))
		cursor.execute(pitchTypeCountSQL)
		try:
			pitchTypeCount = cursor.fetchall()[0][0]
		except:
			pitchTypeCount = 0

		insertLabelsSQL += ", " +pitchType + "_" + "usage"
		insertValuesSQL += ", %s" % str(float(pitchTypeCount)/totalPitchCount)
		pitchTypeStatsSQL = "SELECT " 
		pitchTypeStatsSQL += ", ".join(["AVG(%s)" % label for label in statLabels])
		pitchTypeStatsSQL += """ FROM pitch JOIN atbat ON atbat.id = pitch.atbat_id
			WHERE atbat.pitcher=%i AND pitch_type IN (%s)""" % (pitcherID, ", ".join(allPitchLabels))
		cursor.execute(pitchTypeStatsSQL)
		pitchTypeAvgs = cursor.fetchall()

		# construct an SQL statement from retrieved values
		
		for i in xrange(len(statLabels)):
			statLabel = pitchType + "_" + statLabels[i]
			statValue = pitchTypeAvgs[0][i]
			insertLabelsSQL += ", %s" % statLabel
			insertValuesSQL += ", %s" % str(statValue)
	insertSQL = "INSERT into pitcher_clusters (%s) VALUES (%s)" % (insertLabelsSQL, insertValuesSQL)
	insertSQL = insertSQL.replace('None', "null")
	print insertSQL
	cursor.execute(insertSQL)
	db.commit()
