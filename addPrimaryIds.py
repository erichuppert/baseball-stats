import MySQLdb
verbose = True

db = MySQLdb.connect("localhost", "baseball", "baseball1", "baseball")
cursor = db.cursor()
i = 0
selectGameSQL = "SELECT id, slug FROM game LIMIT %i, 100" % str(i*100)
cursor.execute(selectGameSQL)
games = cursor.fetchall()

for id, slug in games:
	updateAtbatSQL = "UPDATE atbat SET game_id=%i where game_slug='%s'" % (id, slug)
	cursor.execute(updateAtbatSQL)


	


