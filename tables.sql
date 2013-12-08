CREATE TABLE `game` (
  `id` CHAR(32),
  `datetime` DATETIME NOT NULL,
  `day` CHAR(3),
  `league` CHAR(2),
  `game_type` CHAR(1),
  `home_division` CHAR(1),
  `away_division` CHAR(1),
  `gameday_sw` CHAR(1),
  `status` CHAR(32),
  `ind` CHAR(2),
  `inning` INTEGER,
  `outs` INTEGER,
  `top_inning` CHAR(1),
  `away_code` CHAR(3),
  `home_code` CHAR(3),
  `away_team_id` INTEGER,
  `home_team_id` INTEGER,
  `away_name_abbrev` CHAR(3),
  `home_name_abbrev` CHAR(3),
  `away_team_city` CHAR(16),
  `home_team_city` CHAR(16),
  `away_team_runs` INTEGER,
  `home_team_runs` INTEGER,
  `home_win` INTEGER,
  `home_loss` INTEGER,
  `away_win` INTEGER,
  `away_loss` INTEGER,
  `venue` CHAR(32),
  `game_pk` INTEGER,
  `time_zone` CHAR(2),
  `away_team_name` CHAR(16),
  `away_league_id` INTEGER,
  `home_team_name` CHAR(16),
  `home_league_id` INTEGER,
  `away_games_back` FLOAT,
  `home_games_back` FLOAT,
  `home_games_back_wildcard` FLOAT,
  `venue_w_chan_loc` CHAR(16),
  `away_team_hits` INTEGER,
  `home_team_hits` INTEGER,
  `away_team_errors` INTEGER,
  `home_team_errors` INTEGER,
  `away_games_back_wildcard` FLOAT,
  `reason` CHAR(16),
  `tv_station` CHAR(16),
  `venue_id` INTEGER,
  `description` CHAR(100),
  `resume_date` DATETIME,
  `series` CHAR(16),
  `series_num` INTEGER, 
  `ser_games` INTEGER
);



CREATE TABLE pitch (
   des CHAR(255),
   id INTEGER,
   type CHAR(1),
   time DATETIME,
   x FLOAT,
   y FLOAT,
   mt CHAR(255),
   on_1b INTEGER,
   on_2b INTEGER,
   on_3b INTEGER,
   sv_id CHAR(128),
   start_speed float,
   end_speed FLOAT,
   sz_top FLOAT,
   sz_bot FLOAT,
   pfx_x FLOAT,
   pfx_z FLOAT,
   px FLOAT,
   pz FLOAT,
   x0 FLOAT,
   y0 FLOAT,
   z0 FLOAT,
   vx0 FLOAT,
   vy0 FLOAT,
   vz0 FLOAT,
   ax FLOAT,
   ay FLOAT,
   az FLOAT,
   break_y FLOAT,
   break_angle FLOAT,
   break_length FLOAT,
   pitch_type CHAR(4),
   type_confidence FLOAT,
   zone INTEGER,
   nasty INTEGER,
   spin_dir FLOAT,
   spin_rate FLOAT,
   balls INTEGER,
   strikes INTEGER,
   atbat_num INTEGER NOT NULL,
   game_id CHAR(32) NOT NULL
);

CREATE TABLE atbat (
   game_id CHAR(32) NOT NULL,
   num INTEGER NOT NULL,
   b INTEGER,
   s INTEGER,
   o INTEGER,
   time DATETIME,
   batter INTEGER,
   stand CHAR(1),
   b_height  CHAR(32),
   pitcher INTEGER,
   p_throws CHAR(1),
   des  CHAR(255),
   score CHAR(1),
   home_team_runs INTEGER,
   away_team_runs INTEGER,
   event CHAR(128),
   inning INTEGER NOT NULL,
   inning_half  CHAR(1) NOT NULL
);

CREATE TABLE player (

        id INTEGER,
        first CHAR(20),
        last CHAR(20),
        rl CHAR(1),
        position CHAR(2),
        team CHAR(3),
        team_id INTEGER       
);
        
  /*CREATE TABLE umpire (

          position ENUM('first','home','second','third') NOT NULL,
          name CHAR(50),
          id INTEGER,
          url_player CHAR(108) NOT NULL,
          url CHAR(120) NOT NULL
          
  );

  CREATE TABLE coach (

          position CHAR(30),
          first CHAR(20),
          last CHAR(20),
          id INTEGER,
          num INTEGER,
          url_player CHAR(108) NOT NULL,
          url CHAR(120) NOT NULL
          
  );*/Ctrl-C -- exit!
Ctrl-C -- exit!
