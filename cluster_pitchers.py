import MySQLdb
import numpy
# import pdb
from sklearn.cluster import MeanShift, estimate_bandwidth



#initialize db connection
db = MySQLdb.connect("localhost", "baseball", "baseball1", "baseball")
cursor = db.cursor()

#############  retrieve data from database  #############

# clusters will be done by handedness (righty never in cluster with lefty)
throws = 'R'

sql = """SELECT * FROM pitcher_clusters WHERE throws = '%s'""" % throws


cursor.execute(sql)
pitchers = list(cursor.fetchall())

# pdb.set_trace()

#############   clustering  #############

ms = MeanShift()
pitcherVectors = []

for i in xrange(len(pitchers)):
	for j in xrange(len(pitchers[i])):
		if pitchers[i][j] == None:
			pitchers[i] = pitchers[i][:j] + (0.0,) + pitchers[i][j+1:]
	pitcherVectors.append(list(pitchers[i])[2:])
featureVectors = numpy.array(pitcherVectors)
