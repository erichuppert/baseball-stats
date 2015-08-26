import os
import xml.etree.ElementTree as ET
import MySQLdb
import datetime
from download import downloadDirectory
verbose = False


"""Handles migration of all files from xml into the MySQLdb. Requires
that MySQLdb python module is installed."""
def migrate(directory, db):
	cursor = db.cursor()
	for root, dirs, filenames in os.walk(directory):
		if not (len(dirs) == 0 and len(filenames) > 2):
			continue
		print root
		game = ET.parse(root+'/linescore.xml').getroot()
		gameAttribs = game.attrib
		id = gameAttribs['id']
		print id
		#check if the game is already in the database
		checkSQL = "SELECT id FROM game WHERE id = '%s'"%(id)
		cursor.execute(checkSQL)
		if cursor.fetchone():
			#print "Game already in database"
			pass
		#if game not in databse, get game details and add to 'game' table
		else: 		
			if "time_date" in gameAttribs:
				date = gameAttribs["time_date"]
			else:
				date = id[:10] + " " + gameAttribs['time']
			try:
				date = datetime.datetime.strptime(date, '%Y/%m/%d %I:%M')
			except:
				date = datetime.datetime.strptime(date[:10], '%Y/%m/%d') 	
			if gameAttribs['ampm'] == 'PM':
				date += datetime.timedelta(hours=12)
			datetime = date.strftime('%Y-%m-%d %H:%M:%S')

			# we will add the columns mapped to their corresponding value in this hash, then construct the SQL insert from that
			gameAttributesHash = {datetime: datetime, id: id}
			# these are all the values that we want from the gameAttribs hash
			gameAttribKeys = ["id", "datetime", "day", "league", "game_type", "home_division", "away_division",
				"gameday_sw", "status","ind", "inning", "outs", "top_inning", "away_team", "home_team",
				"away_team_id", "home_team_id", "away_name_abbrev", "home_name_abbrev",
				"away_team_city", "home_team_city", "away_team_runs", "home_team_runs", "home_win",
				"home_loss", "away_win", "away_loss", "venue", "game_pk", "time_zone", "away_team_name",
				"away_league_id", "home_team_name", "home_league_id",	"away_games_back", 
				"home_games_back", "home_games_back_wildcard", "venue_w_chan_loc", "away_team_hits",
				"home_team_hits", "away_team_errors", "home_team_errors", "away_games_back_wildcard",
				"reason", "tv_station", "venue_id", "description", "series", "series_num", "ser_games"]
			# we are basically filtering the full dictionary down to just the keys we want
			for key in gameAttribKeys:
				gameAttributesHash[key] = gameAttribs.get("day", "null")

			# in the case when the team is in the lead, we want gb to be 0 rather than '-'
			standingsKeys = ["away_games_back", "home_games_back", "home_games_back_wildcard", "away_games_back_wildcard"]
			for key in standingsKeys:
				if gameAttributesHash[key] == "-":
					gameAttributesHash[key] = 0
			
			insertDict(gameAttributesHash, "game")

		innings_all = ET.parse(root+'/innings_all.xml').getroot()
		innings = innings_all.getchildren()
		for inning in innings:
			inning_num = inning.attrib['num']
			inning_halves = inning.getchildren()
			for half in inning_halves:
				if half.tag == 'bottom':
					inning_half = 'B'
				if half.tag == 'top':
					inning_half = 'T'
				inningevents = half.getchildren()
				for ievent in inningevents:
					if ievent.tag == 'atbat':
						atbatAttribs = ievent.attrib
						abnum = atbatAttribs['num']
						checkSQL = "SELECT num FROM atbat WHERE game_id='%s' and num='%s'"%(id, abnum)
						cursor.execute(checkSQL)
						if cursor.fetchall():
							if verbose:
								print "atbat already in database"
							pass
						else:
							atbatKeys = ["b", "s", "o", "start_tfs_zulu", "batter", "stand", "b_height", "pitcher", "p_throws",
								"des", "score", "home_team_runs", "away_team_runs", "event", "num"]
							atbatDetailsForInsert = filterDict(atbatAttribs, atbatKeys)
							abstfsz = atbatDetailsForInsert["start_tfs_zulu"]
							if abstfsz not in ("", 'null'):
								dt = datetime.datetime.strptime(abstfsz, '%Y-%m-%dT%H:%M:%SZ')
								dt = dt.strftime('%Y-%m-%d %H:%M:%S')
							else:
								dt = 'null'
							atbatDetailsForInsert["start_tfs_zulu"] = dt
							insertDict(atbatDetailsForInsert, "atbat")
						events = ievent.getchildren()
						balls = 0
						strikes = 0
						for event in events:
							if event.tag == 'pitch':
								allPitchAttribs = event.attrib
								pitchid = allPitchAttribs['id']
								checkSQL = "SELECT id FROM pitch WHERE game_id='%s' and atbat_num = '%s' and id = '%s'"%(id, abnum, pitchid)
								cursor.execute(checkSQL)
								if cursor.fetchone():
									#print "pitch already in database"
									pass
								else:
									pitchKeys = ["des", "type", "tfs_zulu", "x", "y", "mt", "on_1b", "on_2b", "on_3b", "sv_id", "start_speed",
										"end_speed", "sz_top", "sz_bot", "pfx_x", "pfx_z", "px", "pz", "x0", "y0", "z0", "vx0", "vy0", "vz0",
										"ax", "ay", "az", "break_y", "break_angle", "break_length", "pitch_type", "type_considence", "zone", "nasty",
										"spin_dir", "spin_rate"]
									pitchAttribs = filterDict(allPitchAttribs, pitchKeys)
									abstfsz = pitchAttribs["tfs_zulu"]
									if abstfsz not in ("", 'null'):
										dt = datetime.datetime.strptime(abstfsz, '%Y-%m-%dT%H:%M:%SZ')
										dt = dt.strftime('%Y-%m-%d %H:%M:%S')
									else:
										dt = 'null'
									pitchAttribs["tfs_zulu"] = dt
									insertDict(pitchAttribs, "pitch")

									#update balls and strikes
									if pitch["type"] in "SX" and strikes < 2:
										strikes += 1
									elif pitch["type"] == 'B':
										balls += 1
							if event.tag == 'runner':
								#do all of the runner attribute stuff
								allRunnerAttribs = event.attrib
								runnerid = allRunnerAttribs['id']
								checkSQL = "SELECT id FROM runner WHERE game_id='%s' and atbat_num ='%s' and id='%s'"%(id, abnum, runnerid)
								cursor.execute(checkSQL)
								if cursor.fetchone():
									"runner already in databse"
								else:
									runnerKeys = ["start", "end", "event", "score", "rbi", "earned"]
									runnerAttribs = filterDict(allRunnerAttribs, runnerKeys)
									insertDict(runnerAttribs, "runner")
		
		playerlist = ET.parse(root+'/players.xml').getroot()
		teams = filter(lambda x: x.tag == "team", playerlist.getchildren())
		for team in teams:
			playerteam = team.attrib['id']
			players = [p for p in team.getchildren() if p.tag == 'player']
			for player in players:
				playerAttribs = player.attrib
				playerid = playerAttribs['id']
				checkSQL = "SELECT id FROM player WHERE id='%s'"%(playerid)
				cursor.execute(checkSQL)
				if not cursor.fetchone():
					# teamid = playerAttribs.get('team_id', 'null')
					first = playerAttribs.get('first', 'null')
					last = playerAttribs.get('last', 'null')
					checkBatsSQL = "SELECT DISTINCT stand FROM atbat WHERE batter='%s'"%(playerid)
					cursor.execute(checkBatsSQL)
					batHands = cursor.fetchall()
					if ('R',) in batHands and ('L',) in batHands:
						bats = 'S'
					elif ('R',) in batHands:
						bats = 'R'
					elif ('L',) in batHands:
						bats = 'L'
					else:
						bats = 'null'
					checkThrowsSQL = "SELECT DISTINCT p_throws from atbat WHERE pitcher='%s' LIMIT 1"%(playerid)
					cursor.execute(checkThrowsSQL)
					pitchHands = cursor.fetchall()
					if ('L',) in pitchHands:
						throws = 'L'
					elif ('R',) in pitchHands:
						throws = 'R'
					else:
						throws='null'
					
					playerSQL="""INSERT INTO player(id, first, last, bats, throws)
						VALUES("{0}","{1}","{2}","{3}","{4}"
						)""".format(playerid, first, last, bats, throws)
					playerSQL = playerSQL.replace('"null"', "null")
					try:
						cursor.execute(playerSQL)
						db.commit()
					except:
						print playerSQL
						db.rollback()
						raise

def insertDict(dict, tableName):
	### This could be necessary, test it!
	# #mysql needs null without quotes, this simply removes the extra quotes
	# gameSQL = gameSQL.replace('"null"', "null")
	qmarks = ', '.join('?' * len(myDict))
	qry = "Insert into %s (%s) Values (%s)" % (tableName, qmarks, qmarks)
	try:
		cursor.execute(qry, myDict.keys() + myDict.values())
		db.commit()
	except:
		db.rollback()
		raise

def filterDict(dict, keys):
	result = {}
	for key in keys:
		result[key] = dict.get("day", "null")
	return result

if __name__ == "__main__":
	db = MySQLdb.connect("localhost", "baseball", "baseball1", "baseball")
	migrate('/media/eric/EHUPPERT700/SABR/mlb-database', db)


