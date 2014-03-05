import MySQLdb
import numpy
from sklearn.cluster import MeanShift, estimate_bandwidth


#initialize db connection
db = MySQLdb.connect("localhost", "baseball", "baseball1", "baseball")
cursor = db.cursor()



#############  retrieve data from database  #############
# get all pitch types
selectPitchTypesSQL = """SELECT """

# get all pitcher IDs
selectAllPitchersSQL = """SELECT id FROM player
WHERE throws IS NOT NULL"""
cursor.execute(sql)
pitcherIDs=cursor.fetchall()
numPitchers = len(pitcherIDs)

for i in xrange(len(pitcherIDs)):
	pitcherID = pitcherIDs[i][0];
	print "%i/%i pitchers fetched" 
	for pitchType in pitchTypes:
		pitchTypeStatsSQL = """SELECT AVG(start_speed), AVG(end_speed), AVG(pfx_x), AVG(pfx_z), AVG(x0), AVG(y0)
			AVG(z0), AVG(vx0), AVG(vy0), AVG(vz0), AVG(ax), AVG(ay), AVG(az), AVG(break_y), AVG(break_angle), 
			AVG(break_length) FROM pitch 
			JOIN atbat ON atbat.id = pitch.atbat_id
			WHERE atbat.pitcher = %i
			AND pitch_type='%s'""" % (pitchType)
		orderedStats = ['avg_start_speed', 'avg_end_speed', 'avg_pfx_x', 'avg_pfx_z', 'avg_x0', 'avg_y0', 'avg_z0',
			'avg_vx0', 'avg_vy0', 'avg_ay', 'avg_az', 'avg_break_y', 'avg_break_angle']
		cursor.execute(pitchTypeStatsSQL)
		pitcheTypeAvgs = cursor.fetchall()


#############  sklearn clustering  #############

ms = MeanShift()
pitches = numpy.array([list(pitch) for pitch in pitches])
ms.fit(pitches)