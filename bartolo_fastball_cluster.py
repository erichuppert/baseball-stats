import MySQLdb
import numpy
from sklearn.cluster import MeanShift, estimate_bandwidth


#initialize db connection
db = MySQLdb.connect("localhost", "baseball", "baseball1", "baseball")
cursor = db.cursor()

#############  retrieve data from database  #############
sql = """SELECT start_speed, end_speed, pfx_x, pfx_z, x0, y0
z0, vx0, vy0, vz0, ax, ay, az, break_y, break_angle, 
break_length FROM pitch 
JOIN atbat ON atbat.game_id=pitch.game_id AND atbat.num=pitch.atbat_num
JOIN game ON pitch.game_id=game.id
JOIN player ON atbat.pitcher=player.id
#WHERE year(game.datetime) IN (2013)
AND player.last='Pomeranz' AND player.first='Drew'
#AND pitch.pitch_type IN ('FT','FF')
AND pitch_type IS NOT NULL"""

cursor.execute(sql)
pitches=cursor.fetchall()


#############  sklearn clustering  #############

ms = MeanShift()
pitches = numpy.array([list(pitch) for pitch in pitches])
ms.fit(pitches)