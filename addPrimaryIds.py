import MySQLdb
import pdb
verbose = True

db = MySQLdb.connect("localhost", "baseball", "baseball1", "baseball")
cursor = db.cursor()
i = 4
selectGamesSQL = "SELECT id, slug FROM game LIMIT %i, 100" % (i*100)
cursor.execute(selectGamesSQL)
games = cursor.fetchall()

while len(games)>0:
	print "i =", i
	for game_id, game_slug in games:
		print game_slug
		updateAtbatsSQL = "UPDATE atbat SET game_id=%i where game_slug='%s'" % (game_id, game_slug)
		cursor.execute(updateAtbatsSQL)
		selectAtbatsSQL = "SELECT id, num FROM atbat WHERE game_slug='%s'" % game_slug
		cursor.execute(selectAtbatsSQL)
		atbats = cursor.fetchall()
		for atbat_id, atbat_num in atbats:
			selectPitchesSQL = "SELECT atbat_index FROM pitch WHERE game_id='%s' AND atbat_num=%i ORDER BY atbat_index ASC" % (game_slug, atbat_num)
			cursor.execute(selectPitchesSQL)
			pitches = cursor.fetchall()
			for j in range(len(pitches)):
				atbat_index = pitches[j][0]
				updatePitchSQL = "UPDATE pitch SET gid=%i, atbat_id=%i, atbat_index=%i WHERE atbat_index=%i AND game_id='%s' AND atbat_num=%i" % (game_id, atbat_id, j, atbat_index, game_slug, atbat_num)
				cursor.execute(updatePitchSQL)
		db.commit()
	i += 1
	selectGamesSQL = "SELECT id, slug FROM game LIMIT %i, 100" % (i*100)
	cursor.execute(selectGamesSQL)
	games = cursor.fetchall()