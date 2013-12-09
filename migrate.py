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
			date = date.strftime('%Y-%m-%d %H:%M:%S')

			day = gameAttribs.get("day", "null")
			l = gameAttribs.get("league", "null")
			gt = gameAttribs.get("game_type", "null")
			hd = gameAttribs.get("home_division", "null")
			ad = gameAttribs.get("away_division", "null")
			gdsw = gameAttribs.get("gameday_sw", "null")
			s = gameAttribs.get("status", "null")
			ind = gameAttribs.get("ind", "null")
			inn = gameAttribs.get("innings", "null") 
			outs = gameAttribs.get("outs", "null")
			ti = gameAttribs.get("top_inning", "null")
			ac = gameAttribs.get("away_code", "null")
			hc = gameAttribs.get("home_code", "null")
			ati = gameAttribs.get("away_team_id", "null")
			hti = gameAttribs.get("home_team_id", "null")
			ana = gameAttribs.get("away_name_abbrev", "null")
			hna = gameAttribs.get("home_name_abbrev", "null")
			atc = gameAttribs.get("away_team_city", "null")
			htc = gameAttribs.get("home_team_city", "null")
			atr = gameAttribs.get("away_team_runs", "null")
			htr = gameAttribs.get("home_team_runs", "null")
			hw = gameAttribs.get("home_win", "null")
			aw = gameAttribs.get("away_win", "null")
			al = gameAttribs.get("away_loss", "null")
			hl = gameAttribs.get("home_loss", "null")
			ven = gameAttribs.get("venue", "null")
			gpk = gameAttribs.get("game_pk", "null")
			tz = gameAttribs.get("home_time_zone", "null")
			atn = gameAttribs.get("away_team_name", "null")
			ali = gameAttribs.get("away_league_id", "null")
			htn = gameAttribs.get("home_team_name", "null")
			hli = gameAttribs.get("home_league_id", "null")
			agb = gameAttribs.get("away_games_back", "null")
			if agb == '-':
				agb = '0'
			hgb = gameAttribs.get("home_games_back", "null")
			if hgb == '-':
				hgb = '0'
			hgbw = gameAttribs.get("home_games_back_wildcard", "null")
			if hgbw == '-':
				hgbw = '0'
			vwc = gameAttribs.get("venue_w_chan_loc", "null")
			ath = gameAttribs.get("away_team_hits", "null")
			hth = gameAttribs.get("home_team_hits", "null")
			ate = gameAttribs.get("away_team_errors", "null")
			hte = gameAttribs.get("home_team_errors", "null")
			agbw = gameAttribs.get("away_games_back_wildcard", "null")
			if agbw == '-':
				agbw = '0'
			reason = gameAttribs.get("reason", "null")
			tvs = gameAttribs.get("tv_station", "null")
			vid = gameAttribs.get("venue_id", "null")
			des = gameAttribs.get("description", "null")
			ser = gameAttribs.get("series", "null")
			sern = gameAttribs.get("series_num", "null")
			sg = gameAttribs.get("ser_games", "null")

			gameSQL = """INSERT INTO game(id, datetime, day,
			 	league, game_type, home_division, away_division, gameday_sw, status,
				ind, inning, outs, top_inning, away_code, home_code, away_team_id, 
				home_team_id, away_name_abbrev,
				home_name_abbrev, away_team_city, home_team_city, away_team_runs,
				home_team_runs, home_win, home_loss,
				away_win, away_loss, venue, game_pk, time_zone, away_team_name,
				away_league_id, home_team_name, home_league_id,
				away_games_back, home_games_back,
				home_games_back_wildcard, venue_w_chan_loc, away_team_hits,
				home_team_hits, away_team_errors, home_team_errors, 
				away_games_back_wildcard, reason, 
				tv_station, venue_id, description, 
				series, series_num, ser_games) 
				VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}',
					'{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}',
					'{19}','{20}','{21}','{22}','{23}','{24}','{25}','{26}',"{27}",
					'{28}','{29}','{30}','{31}','{32}','{33}','{34}','{35}','{36}',
					'{37}','{38}','{39}','{40}','{41}','{42}','{43}','{44}','{45}',
					'{46}','{47}','{48}','{49}')""".format(id, date, day, l,\
					gt, hd, ad, gdsw, s, ind, inn, outs, ti, ac, hc, ati, hti, ana,\
					hna, atc, htc, atr, htr, hw, hl, aw, al, ven, gpk, tz, atn, ali,\
					htn, hli, agb, hgb, hgbw, vwc, ath, hth, ate, hte, agbw,\
					reason, tvs, vid, des, ser, sern, sg)

			#mysql needs null without quotes, this simply removes the extra quotes
			gameSQL = gameSQL.replace("'null'", "null")
			if verbose:
				print gameSQL
			try:
				cursor.execute(gameSQL)
				db.commit()
			except:
				print gameSQL
				db.rollback()
			#end game attributes

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
							b = atbatAttribs.get('b', 'null')
							s = atbatAttribs.get('s', 'null')
							o = atbatAttribs.get('o', 'null')
							abstfsz = atbatAttribs.get('start_tfs_zulu', 'null')
							if abstfsz != "" and abstfsz != 'null':
								dt = datetime.datetime.strptime(abstfsz, '%Y-%m-%dT%H:%M:%SZ')
								dt = dt.strftime('%Y-%m-%d %H:%M:%S')
							else:
								dt = 'null'
							batter = atbatAttribs.get('batter', 'null')
							stand = atbatAttribs.get('stand', 'null')
							bheight = atbatAttribs.get('b_height', 'null')
							pitcher = atbatAttribs.get('pitcher', 'null')
							pthrow = atbatAttribs.get('p_throws', 'null')
							des = atbatAttribs.get('des', 'null')
							score = atbatAttribs.get('score', 'null')
							htr = atbatAttribs.get('home_team_runs', 'null')
							atr = atbatAttribs.get('away_team_runs', 'null')
							event = atbatAttribs.get('event', 'null')

							atbatSQL = """INSERT INTO atbat(game_id, num, b, s, o,
								time, batter, stand, b_height,
								pitcher, p_throws, des, score, home_team_runs,
								away_team_runs, event, inning, inning_half) VALUES ("{0}",
								"{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}",
								"{10}","{11}","{12}","{13}","{14}","{15}","{16}","{17}")
								""".format(id, abnum, b, s, o, dt,\
								batter, stand, bheight, pitcher, pthrow, des, \
								score, htr, atr, event, inning_num, inning_half)

							atbatSQL = atbatSQL.replace('"null"', "null")

							if verbose:
								print atbatSQL

							try:
								cursor.execute(atbatSQL)
								db.commit()
							except:
								print atbatSQL
								db.rollback()
								raise
						events = ievent.getchildren()
						balls = 0
						strikes = 0
						for event in events:
							if event.tag == 'pitch':
								pitchAttribs = event.attrib
								pitchid = pitchAttribs['id']
								checkSQL = "SELECT id FROM pitch WHERE game_id='%s' and atbat_num = '%s' and id = '%s'"%(id, abnum, pitchid)
								cursor.execute(checkSQL)
								if cursor.fetchone():
									#print "pitch already in database"
									pass
								else:
									des = pitchAttribs.get('des', 'null')
									ptype = pitchAttribs.get('type', 'null')
									abstfsz = pitchAttribs.get('tfs_zulu', 'null')
									if abstfsz != "" and abstfsz != 'null':
										dt = datetime.datetime.strptime(abstfsz, '%Y-%m-%dT%H:%M:%SZ')
										dt = dt.strftime('%Y-%m-%d %H:%M:%S')
									else:
										dt = 'null'
									x = pitchAttribs.get('x', 'null')
									y = pitchAttribs.get('y', 'null')
									mt = pitchAttribs.get('mt', 'null')
									if mt and verbose:
										print 'mt not None for pitch', pitchid
									first = pitchAttribs.get('on_1b', 'null')
									second = pitchAttribs.get('on_2b', 'null')
									third = pitchAttribs.get('on_3b', 'null')
									svid = pitchAttribs.get('sv_id', 'null')
									ss = pitchAttribs.get('start_speed', 'null')
									es = pitchAttribs.get('end_speed', 'null')
									sztop = pitchAttribs.get('sz_top', 'null')
									szbot = pitchAttribs.get('sz_bot', 'null')
									pfxx = pitchAttribs.get('pfx_x', 'null')
									pfxz = pitchAttribs.get('pfx_z', 'null')
									px = pitchAttribs.get('px', 'null')
									pz = pitchAttribs.get('pz', 'null')
									x0 = pitchAttribs.get('x0', 'null')
									y0 = pitchAttribs.get('y0', 'null')
									z0 = pitchAttribs.get('z0', 'null')
									vx0 = pitchAttribs.get('vx0', 'null')
									vy0 = pitchAttribs.get('vy0', 'null')
									vz0 = pitchAttribs.get('vz0', 'null')
									ax = pitchAttribs.get('ax', 'null')
									ay = pitchAttribs.get('ay', 'null')
									az = pitchAttribs.get('az', 'null')
									breaky = pitchAttribs.get('break_y', 'null')
									breakangle = pitchAttribs.get('break_angle', 'null')
									breaklength = pitchAttribs.get('break_length', 'null') 
									pitchtype = pitchAttribs.get('pitch_type', 'null')
									type_confidence = pitchAttribs.get('type_confidence', 'null')
									zone = pitchAttribs.get('zone', 'null')
									nasty = pitchAttribs.get('nasty', 'null')
									spindir = pitchAttribs.get('spin_dir', 'null')
									spinrate = pitchAttribs.get('spin_rate', 'null')

									

									pitchSQL = """INSERT INTO pitch(des, id, type, time, x, y,
										mt, on_1b, on_2b, on_3b, sv_id, start_speed, end_speed,
										sz_top, sz_bot, pfx_x, pfx_z, px, pz, x0, y0, z0, vx0, vy0,
										vz0, ax, ay, az, break_y, break_angle, break_length, pitch_type,
										type_confidence, zone, nasty, spin_dir, spin_rate, balls, strikes,
										atbat_num, game_id) VALUES("{0}","{1}","{2}","{3}","{4}","{5}",
										"{6}","{7}","{8}","{9}","{10}","{11}","{12}","{13}","{14}","{15}",
										"{16}","{17}","{18}","{19}","{20}","{21}","{22}","{23}","{24}",
										"{25}","{26}","{27}","{28}","{29}","{30}","{31}","{32}","{33}",\
										"{34}","{35}","{36}","{37}","{38}","{39}", "{40}")""".format(des, pitchid,\
											ptype, dt, x, y, mt, first,	second, third, svid, ss, es, sztop,\
											szbot, pfxx, pfxz, px, pz, x0, y0, z0, vx0, vy0, vz0, ax, ay,\
											az, breaky, breakangle, breaklength, pitchtype, type_confidence,\
											zone, nasty, spindir, spinrate, balls, strikes, abnum, id)
									pitchSQL = pitchSQL.replace('"null"', "null")
									try:
										cursor.execute(pitchSQL)
										db.commit()
									except:
										print pitchSQL
										db.rollback()
										raise

									#update balls and strikes
									if ptype in "SX" and strikes < 2:
										strikes += 1
									elif ptype == 'B':
										balls += 1
									elif ptype not in "SXB":
										print 'pitch', str(pitchid), 'from game', str(id), 'has type', str(ptype)
							# if event.tag == 'runner':
							# 	#do all of the runner attribute stuff
							# 	runnerAttribs = event.attrib
							# 	runnerid = runnerAttribs['id']
							# 	checkSQL = "SELECT id FROM runner WHERE game_id='%s' and atbat_num ='%s' and id='%s'"%(id, abnum, runnerid)
							# 	cursor.execute(checkSQL)
							# 	if cursor.fetchone():
							# 		"runner already in databse"
							# 	else:
							# 		start = runnerAttribs.get('start', 'null')
							# 		end = runnerAttribs.get('end', 'null')
							# 		event = runnerAttribs.get('event', 'null')
							# 		score = runnerAttribs.get('score', 'null')
							# 		rbi = runnerAttribs.get('rbi', 'null')
							# 		earned = runnerAttribs.get('earned', 'null')
							# 		runnerSQL = """INSERT INTO runner(id, start, end,
							# 			event, score, rbi, earned, game_id, atbat_num)
							# 			VALUES('{0}','{1}','{2}','{3}','{4}','{5}',
							# 			'{6}','{7}','{8}')""".format(runnerid, start,\
							# 			end, event, score, rbi, earned, id, abnum)
							# 		print runnerSQL

							# 		runnerSQL.replace("'null'", "null")
							# 		try:
							# 			cursor.execute(runnerSQL)
							# 			db.commit()
							# 		except:
							# 			db.rollback()
							# 			raise
		
		playerlist = ET.parse(root+'/players.xml').getroot()
		date = datetime.datetime.strptime(playerlist.attrib['date'], '%B %d, %Y')
		teams = [t for t in playerlist.getchildren() if t.tag == 'team']
		for team in teams:
			playerteam = team.attrib['id']
			players = [p for p in team.getchildren() if p.tag == 'player']
			for player in players:
				playerAttribs = player.attrib
				playerid = playerAttribs['id']
				checkSQL = "SELECT id FROM player WHERE id='%s' and team='%s'"%(playerid, playerteam)
				cursor.execute(checkSQL)
				if not cursor.fetchone():
					teamid = playerAttribs.get('team_id', 'null')
					first = playerAttribs.get('first', 'null')
					last = playerAttribs.get('last', 'null')
					position = playerAttribs.get('position', 'null')
					rl = playerAttribs.get('rl', 'null')

					playerSQL="""INSERT INTO player(id, first, last, rl, position,
						team, team_id) VALUES("{0}","{1}","{2}","{3}","{4}","{5}",
						"{6}")""".format(playerid, first, last, rl, position,\
						playerteam, teamid)
					playerSQL = playerSQL.replace('"null"', "null")
					try:
						cursor.execute(playerSQL)
						db.commit()
					except:
						print playerSQL
						db.rollback()
						raise


if __name__ == "__main__":
	db = MySQLdb.connect("localhost", "baseball", "baseball1", "baseball")
	migrate('/home/eric/Projects/mlb-database', db)


