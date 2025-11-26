CREATE TABLE game (
	"game_id" INT,
	"season" VARCHAR(100),
	"type" VARCHAR(100),
	"date_time_GMT" DATETIME,
	"away_team_id" INT,
	"home_team_id" INT,
	"away_goals" INT,
	"home_goals" INT,
	"outcome" VARCHAR(100),
	"home_rink_side_start" VARCHAR(100),
	"venue" VARCHAR(100),
	PRIMARY KEY("game_id")
);

CREATE TABLE game_goalie_stats (
	"game_id" INT,
	"player_id" INT,
	"team_id" INT,
	"timeOnIce" INT,
	"assists" INT,
	"goals" INT,
	"pim" INT,
	"shots" INT,
	"saves" INT,
	"powerPlaySaves" INT,
	"shortHandedSaves" INT,
	"evenSaves" INT,
	"shortHandedShotsAgainst" INT,
	"evenShotsAgainst" INT,
	"powerPlayShotsAgainst" INT,
	"decision" VARCHAR(100),
	"savePercentage" FLOAT,
	"powerPlaySavePercentage" FLOAT,
	"evenStrengthSavePercentage" FLOAT,
	PRIMARY KEY("game_id","player_id")
);

CREATE TABLE game_goals (
	"game_goal_id" INT,
	"play_id" VARCHAR(100),
	"strength" VARCHAR(100),
	"gameWinningGoal" VARCHAR(100),
	"emptyNet" VARCHAR(100),
	PRIMARY KEY("game_goal_id")
);

CREATE TABLE game_officials (
	"game_id" INT,
	"official_name" VARCHAR(100),
	"official_type" VARCHAR(100),
	PRIMARY KEY("game_id","official_name")
);

CREATE TABLE game_penalties (
	"play_id" VARCHAR(100),
	"penaltySeverity" VARCHAR(100),
	"penaltyMinutes" INT,
	PRIMARY KEY("play_id")
);

CREATE TABLE game_plays (
	"play_id" VARCHAR(100),
	"game_id" INT,
	"team_id_for" INT,
	"team_id_against" INT,
	"event" VARCHAR(100),
	"secondaryType" VARCHAR(100),
	"x" INT,
	"y" INT,
	"period" INT,
	"periodType" VARCHAR(100),
	"periodTime" INT,
	"periodTimeRemaining" INT,
	"dateTime" DATETIME,
	"goals_away" INT,
	"goals_home" INT,
	"description" VARCHAR(100),
	"st_x" INT,
	"st_y" INT,
	PRIMARY KEY("play_id")
);

CREATE TABLE game_plays_players (
	"play_id" VARCHAR(100),
	"game_id" INT,
	"player_id" INT,
	"playerType" VARCHAR(100),
	PRIMARY KEY("play_id","game_id","player_id")
);

CREATE TABLE game_scratches (
	"game_id" INT,
	"team_id" INT,
	"player_id" INT,
	PRIMARY KEY("game_id","team_id","player_id")
);

CREATE TABLE game_shifts (
	"game_id" INT,
	"player_id" INT,
	"period" INT,
	"shift_start" INT,
	"shift_end" INT,
	PRIMARY KEY("game_id","player_id","shift_start","shift_end")
);

CREATE TABLE game_skater_stats (
	"game_id" INT,
	"player_id" INT,
	"team_id" INT,
	"timeOnIce" INT,
	"assists" INT,
	"goals"	INT,
	"shots"	INT,
	"hits" INT,
	"powerPlayGoals" INT,
	"powerPlayAssists" INT,
	"penaltyMinutes" INT,
	"faceOffWins" INT,
	"faceoffTaken" INT,
	"takeaways"	INT,
	"giveaways"	INT,
	"shortHandedGoals" INT,
	"shortHandedAssists" INT,
	"blocked" INT,
	"plusMinus" INT,
	"evenTimeOnIce"	INT,
	"shortHandedTimeOnIce" INT,
	"powerPlayTimeOnIce" INT,
	PRIMARY KEY("game_id","player_id")
);

CREATE TABLE game_teams_stats (
	"game_id" INT,
	"team_id" INT,
	"HoA" VARCHAR(100),
	"won" VARCHAR(100),
	"settled_in" VARCHAR(100),
	"head_coach" VARCHAR(100),
	"goals"	INT,
	"shots"	INT,
	"hits" INT,
	"pim" INT,
	"powerPlayOpportunities" INT,
	"powerPlayGoals" INT,
	"faceOffWinPercentage" FLOAT,
	"giveaways"	INT,
	"takeaways"	INT,
	"blocked" INT,
	"startRinkSide"	VARCHAR(100),
	PRIMARY KEY("game_id","team_id")
);

CREATE TABLE player_info (
	"player_id"	INT,
	"firstName" VARCHAR(100),
	"lastName" VARCHAR(100),
	"nationality" VARCHAR(100),
	"birthCity" VARCHAR(100),
	"primaryPosition" VARCHAR(100),
	"birthDate"	DATE,
	"birthStateProvince" VARCHAR(100),
	"height" VARCHAR(100),
	"weight" INT,
	"shootsCatches" VARCHAR(100),
	PRIMARY KEY("player_id")
);

CREATE TABLE team_info (
	"team_id" INT,
	"shortName"	VARCHAR(100),
	"teamName" VARCHAR(100),
	"abbreviation" VARCHAR(100),
	PRIMARY KEY("team_id")
);