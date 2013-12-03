import os
import xml.etree.ElementTree as ET
import MySQLdb
import datetime
from download import downloadDirectory
verbose = True


"""Handles migration of all files from xml into the MySQLdb. Requires
that MySQLdb python module is installed."""
def migrate(directory, db):
	for root, dirs, filenames in os.walk(directory):
		if len(dirs) == 0 and len(filenames) > 1:
			gameDir = root
		else:
			continue
	cursor = db.cursor()


	game = ET.parse('/home/eric/Desktop/bb/linescore.xml').getroot()
	gameAttribs = game.attrib
	id = gameAttribs.get("id", "null")

	#check if the game is already in the database
	checkSQL = "SELECT COUNT(1) FROM game WHERE id = '%s'"%(id)
	cursor.execute(checkSQL)

	if cursor.fetchone()[0]:
		print "Game already in database"
	#if game not in databse, get game details and add to 'game' table
	else: 		
		gdl = gameAttribs.get("gameday_link", "null")
		date = gameAttribs["time_date"]
		date = datetime.datetime.strptime(date, '%Y/%m/%d %I:%M')
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
		tz = gameAttribs.get("time_zone", "null")
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
		hpl = gameAttribs.get("home_preview_link", "null")
		reason = gameAttribs.get("reason", "null")
		tvs = gameAttribs.get("tv_station", "null")
		apl = gameAttribs.get("away_preview_link", "null")
		vid = gameAttribs.get("venue_id", "null")
		des = gameAttribs.get("description", "null")
		mtvl = gameAttribs.get("mlbtv_link", "null")
		wl = gameAttribs.get("wrapup_link", "null")
		rd = gameAttribs.get("resume_date", "null")
		if rd != "null":
			rd = datetime.datetime.strptime(rd, '%Y/%m/%d %I:%M')
			rd = date.strftime('%Y-%m-%d %H:%M:%S')
		ser = gameAttribs.get("series", "null")
		sern = gameAttribs.get("series_num", "null")
		sg = gameAttribs.get("ser_games", "null")
		pstv = gameAttribs.get("postseason_tv_link", "null")

		gameSQL = """INSERT INTO game(id, gameday_link, datetime, day,
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
			away_games_back_wildcard, home_preview_link, reason, 
			tv_station, away_preview_link, venue_id, description,
			mlbtv_link, wrapup_link, resume_date, series, series_num,
			ser_games, postseason_tv_link) 
			VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}',
				'{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}',
				'{19}','{20}','{21}','{22}','{23}','{24}','{25}','{26}','{27}',
				'{28}','{29}','{30}','{31}','{32}','{33}','{34}','{35}','{36}',
				'{37}','{38}','{39}','{40}','{41}','{42}','{43}','{44}','{45}',
				'{46}','{47}','{48}','{49}','{50}','{51}','{52}','{53}','{54}',
				'{55}','{56}')""".format(id, gdl, date, day, l,\
				gt, hd, ad, gdsw, s, ind, inn, outs, ti, ac, hc, ati, hti, ana,\
				hna, atc, htc, atr, htr, hw, hl, aw, al, ven, gpk, tz, atn, ali,\
				htn, hli, agb, hgb, hgbw, vwc, ath, hth, ate, hte, agbw, hpl,\
				reason, tvs, apl, vid, des, mtvl, wl, rd, ser, sern, sg, pstv)

		#mysql needs null without quotes, this simply removes the extra quotes
		gameSQL = gameSQL.replace("'null'", "null")

		try:
			cursor.execute(gameSQL)
			db.commit()
		except:
			#if something goes wrong, don't add any changes to db
			db.rollback()
		#end game attributes

	innings_all = ET.parse(gameDir+'/innings_all.xml').getroot()
	innings = innings_all.getchildren()
	for inning in innings:
		inning_num = inning.attrib['num']
		inning_halves = inning.getchildren()
		for half in inning_halves:
			inning_half = half.tag
			inningevents = half.getchildren()
			for ievent in inningevents:
				if ievent.tag == 'event':
					pass
					#check for all the possible types of events
				if ievent.tag == 'atbat':
					atbatAttribs = atbat.attrib
					abnum = atbatAttribs['num']
					checkSQL = "SELECT * FROM atbat WHERE game_id='%s' and num='%s'"%(id, abnum)
					cursor.execute(checkSQL)
					if cursor.fetchone():
						print "atbat already in database"
					else:
						b = atbatAttribs.get('b', 'null')
						s = atbatAttribs.get('s', 'null')
						o = atbatAttribs.get('o', 'null')
						abstfsz = atbatAttribs.get('start_tfs_zulu', 'null')
						dt = datetime.datetime.strptime(abstfsz, '%Y-%m-%dT%H:%M:%SZ')
						dt = dt.strftime('%Y-%m-%d %H:%M:%S')
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

						atbatSQL = """INSERT INTO atbat(game_id, num, b, s, o,\
							time, batter, stand, b_height,\
							pitcher, p_throws, des, score, home_team_runs,\
							away_team_runs, event, inning, inning_half) VALUES ('{0}',\
							'{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}',\
							'{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}'\
							)""".format(id, abnum, b, s, o, abstfsz,\
							batter, stand, bheight, pitcher, pthrow, des, \
							score, htr, atr, event, inning_num, inning_half)

						atbatSQL = atbatSQL.replace("'null'", "null")
						print atbatSQL

						try:
							cursor.execute(atbatSQL)
							db.commit()
						except:
							db.rollback()
							raise('atbatdb error')
					events = ievent.getchildren()
					for event in events:
						if event.tag == 'pitch':
							pitchAttribs = event.attrib
							checkSQL = pitchAttribs
							#do all of the pitch attribute stuff
							pass
						if event.tag == 'runner':
							#do all of the runner attribute stuff
							pass


db = MySQLdb.connect("localhost", "baseball", "baseball1", "baseball")
migrate('/home/eric/Desktop', db)