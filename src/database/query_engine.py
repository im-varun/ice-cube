import os
import sys
from typing import Any, Optional, cast

ROOT_DIR_NAME = "ice-cube"
curr_path = os.path.dirname(__file__)
idx = curr_path.find(ROOT_DIR_NAME) + len(ROOT_DIR_NAME)
ROOT_PATH = curr_path[:idx]
LIB_PATH = os.path.join(ROOT_PATH, "lib")
if LIB_PATH != sys.path[0]:
    print("inserting to the path")
    sys.path.insert(0, LIB_PATH)
import pymssql


class QueryEngine:
    """
    Available methods:
    - close()
    - execute_refreshdb()

    Avaiilable Querys
    - execute_birthdaycurseanalysis()
    - execute_headtohead()
    - execute_homerinksideadvantage()
    - execute_longestgames()
    - execute_mostcommonplaytypes()
    - execute_mostpenalizedplayers()
    - execute_playerswhoscorebutnotassist()
    - execute_playerswithlongestavgshift()
    - execute_playerswithmostassists()
    - execute_revengegameeffect()
    - execute_topscoringplayers()
    - execute_topshootingteams()
    """

    def __init__(self, server: str, database: str, user: str, password: str) -> None:
        """
        Initialize the QueryEngine with database connection parameters.

        Args:
            server (str): The database server address.
            database (str): The name of the database.
            user (str): The username for database authentication.
            password (str): The password for database authentication.
        """
        self._conn = pymssql.connect(server=server, database=database, user=user, password=password)
        self._cursor = self._conn.cursor(as_dict=True)

    def close(self) -> None:
        """
        Close the database connection and cursor.
        """
        if self._cursor:
            self._cursor.close()

        if self._conn:
            self._conn.close()

    def execute_refreshdb(self) -> Optional[int]:
        """
        Execute the database refresh process by dropping existing tables
        and re-populating them.

        Returns:
            Optional[int]: Returns 500 if an error occurs, otherwise None.
        """
        status = self._drop()
        if status == 500:
            return status

        status = self._populate()
        if status == 500:
            return status

    def _drop(self) -> Optional[int]:
        """
        Drop existing database tables using the drop SQL script.

        Returns:
            Optional[int]: Returns 500 if an error occurs, otherwise None.
        """
        drop_sql_file = "./sql/drop.sql"

        if not os.path.isfile(drop_sql_file):
            return 500

        try:
            self._execute_sql_file(drop_sql_file)

        except Exception:
            return 500

    def _populate(self) -> Optional[int]:
        """
        Populate the database using the schema and populate SQL scripts.

        Returns:
            Optional[int]: Returns 500 if an error occurs, otherwise None.
        """
        schema_sql_file = "./sql/schema.sql"
        populate_sql_file = "./sql/populate.sql"

        if not os.path.isfile(schema_sql_file):
            return 500

        if not os.path.isfile(populate_sql_file):
            return 500

        try:
            self._execute_sql_file(schema_sql_file)
            self._execute_sql_file(populate_sql_file, with_batching=True)

        except Exception:
            return 500

    def _execute_sql_file(self, sql_file: str, with_batching: bool = False) -> None:
        """
        Execute SQL statements from a file, optionally using batching.

        Args:
            sql_file (str): The path to the SQL file.
            with_batching (bool): Whether to execute SQL statements in batches.
        """
        try:
            if with_batching:
                batch = []
                batch_counter = 0

                BATCH_LIMIT = 10000

                with open(sql_file, "r") as file:
                    for line in file:
                        batch.append(line)

                        if len(batch) >= BATCH_LIMIT:
                            batch_counter += 1

                            sql_statements = "".join(batch)
                            self._cursor.execute(sql_statements)
                            self._conn.commit()

                            batch = []

                if batch:
                    batch_counter += 1

                    sql_statements = "".join(batch)
                    self._cursor.execute(sql_statements)
                    self._conn.commit()

            else:
                with open(sql_file, "r") as file:
                    sql_statements = file.read()
                    self._cursor.execute(sql_statements)
                    self._conn.commit()

        except Exception:
            if self._conn:
                self._conn.rollback()

        finally:
            self._cursor.close()
            self._conn.close()

    def execute_query(self, query: str) -> list[dict[str, Any]] | int:
        """
        Execute a given SQL query and return the results.

        Args:
            query (str): The SQL query to execute.

        Returns:
            list[dict[str, Any]] | int: The query results as a list of dictionaries,
            or 500 if an error occurs.
        """
        try:
            self._cursor.execute(query)

            rows = self._cursor.fetchall()
            rows = cast(list[dict[str, Any]], rows)

            return rows

        except Exception:
            return 500

    def execute_headtohead(
        self,
        player1_firstname: str,
        player1_lastname: str,
        player2_firstname: str,
        player2_lastname: str,
    ) -> list[dict[str, Any]] | int:
        """
        Execute a head-to-head comparison query between two players.

        Args:
            player1_firstname (str): First name of first player.
            player1_lastname (str): Last name of first player.
            player2_firstname (str): First name of second player.
            player2_lastname (str): Last name of second player.

        Returns:
            list[dict[str, Any]] | int: The query results as a list of dictionaries,
            or 500 if an error occurs.
        """
        try:
            query = """
            WITH PlayerGames AS (
                SELECT
                    p.player_id,
                    p.firstName + ' ' + p.lastName AS player_name,
                    s.game_id,
                    g.date_time_GMT,
                    s.goals,
                    s.assists,
                    s.shots,
                    s.hits,
                    s.timeOnIce,
                    s.plusMinus
                FROM game_skater_stats s
                JOIN player_info p ON s.player_id = p.player_id
                JOIN game g ON s.game_id = g.game_id
                WHERE (p.firstName = %s AND p.lastName = %s)
                OR (p.firstName = %s AND p.lastName = %s)
            )
            SELECT
                pg1.player_name AS player_1,
                pg2.player_name AS player_2,
                COUNT(*) AS matchups,
                SUM(pg1.goals) AS p1_goals,
                SUM(pg2.goals) AS p2_goals,
                SUM(pg1.assists) AS p1_assists,
                SUM(pg2.assists) AS p2_assists,
                SUM(pg1.shots) AS p1_shots,
                SUM(pg2.shots) AS p2_shots,
                SUM(pg1.hits) AS p1_hits,
                SUM(pg2.hits) AS p2_hits,
                AVG(pg1.plusMinus) AS p1_avg_plus_minus,
                AVG(pg2.plusMinus) AS p2_avg_plus_minus
            FROM PlayerGames pg1
            JOIN PlayerGames pg2 ON pg1.game_id = pg2.game_id AND pg1.player_id < pg2.player_id
            GROUP BY pg1.player_name, pg2.player_name;
            """
            self._cursor.execute(
                query, (player1_firstname, player1_lastname, player2_firstname, player2_lastname)
            )

            rows = self._cursor.fetchall()
            rows = cast(list[dict[str, Any]], rows)

            return rows

        except Exception:
            return 500

    def execute_revengegameeffect(self) -> list[dict[str, Any]] | int:
        """
        Execute a query to analyze the revenge game effect for players.

        Returns:
            list[dict[str, Any]] | int: The query results as a list of dictionaries,
            or 500 if an error occurs.
        """
        try:
            query = """
            SELECT
                p.firstName + ' ' + p.lastName AS player_name,
                t.teamName AS opponent_team,
                COUNT(DISTINCT s.game_id) AS revenge_games,
                SUM(s.goals) AS total_goals,
                SUM(s.assists) AS total_assists,
                SUM(s.hits) AS total_hits,
                SUM(s.shots) AS total_shots
            FROM game_skater_stats s
            JOIN player_info p ON s.player_id = p.player_id
            JOIN game g ON s.game_id = g.game_id
            JOIN team_info t ON (g.home_team_id = t.team_id OR g.away_team_id = t.team_id)
            WHERE t.team_id != s.team_id
                AND EXISTS (
                    SELECT 1 FROM game_skater_stats s2
                    WHERE s2.player_id = s.player_id
                        AND s2.team_id = t.team_id
                        AND s2.game_id < s.game_id
                )
            GROUP BY p.player_id, p.firstName, p.lastName, t.team_id, t.teamName
            HAVING COUNT(DISTINCT s.game_id) >= 1
            ORDER BY SUM(s.goals) + SUM(s.assists) DESC;
            """
            self._cursor.execute(query)

            rows = self._cursor.fetchall()
            rows = cast(list[dict[str, Any]], rows)

            return rows

        except Exception:
            return 500

    def execute_homerinksideadvantage(self) -> list[dict[str, Any]] | int:
        """
        Execute a query to analyze the home rink side advantage in games.

        Returns:
            list[dict[str, Any]] | int: The query results as a list of dictionaries,
            or 500 if an error occurs.
        """
        try:
            query = """
            SELECT
                g.home_rink_side_start,
                COUNT(*) AS total_games,
                SUM(CASE WHEN ts.won = 'True' AND ts.HoA = 'home' THEN 1 ELSE 0 END) AS
                home_wins,
                ROUND(AVG(CAST(ts.goals AS FLOAT)), 2) AS avg_goals,
                ROUND(AVG(CAST(ts.faceOffWinPercentage AS FLOAT)), 2) AS avg_faceoff_pct
            FROM game g
            JOIN game_teams_stats ts ON g.game_id = ts.game_id
            WHERE g.home_rink_side_start IS NOT NULL
            GROUP BY g.home_rink_side_start;
            """
            self._cursor.execute(query)

            rows = self._cursor.fetchall()
            rows = cast(list[dict[str, Any]], rows)

            return rows

        except Exception:
            return 500

    def execute_birthdaycurseanalysis(self) -> list[dict[str, Any]] | int:
        """
        Execute a query to analyze the birthday curse effect for players.

        Returns:
            list[dict[str, Any]] | int: The query results as a list of dictionaries,
            or 500 if an error occurs.
        """
        try:
            query = """
            SELECT
                p.firstName + ' ' + p.lastName AS player_name,
                p.birthDate,
                g.date_time_GMT AS game_date,
                s.goals,
                s.assists,
                s.shots,
                s.plusMinus
            FROM game_skater_stats s
            JOIN player_info p ON s.player_id = p.player_id
            JOIN game g ON s.game_id = g.game_id
            WHERE MONTH(p.birthDate) = MONTH(g.date_time_GMT)
                AND DAY(p.birthDate) = DAY(g.date_time_GMT)
            ORDER BY g.date_time_GMT DESC;
            """
            self._cursor.execute(query)

            rows = self._cursor.fetchall()
            rows = cast(list[dict[str, Any]], rows)

            return rows

        except Exception:
            return 500

    def execute_mostpenalizedplayers(self) -> list[dict[str, Any]] | int:
        """
        Execute a query to find the top 10 most penalized players.

        Returns:
            list[dict[str, Any]] | int: The query results as a list of dictionaries,
            or 500 if an error occurs.
        """
        try:
            query = """
            SELECT TOP 10
                player_info.firstName + ' ' + player_info.lastName AS player_name,
                SUM(game_skater_stats.penaltyMinutes) AS total_penalty_minutes
            FROM game_skater_stats
            JOIN player_info ON game_skater_stats.player_id = player_info.player_id
            GROUP BY player_info.firstName, player_info.lastName
            ORDER BY total_penalty_minutes DESC;
            """
            self._cursor.execute(query)

            rows = self._cursor.fetchall()
            rows = cast(list[dict[str, Any]], rows)

            return rows

        except Exception:
            return 500

    def execute_mostcommonplaytypes(self) -> list[dict[str, Any]] | int:
        """
        Execute a query to find the most common play types.

        Returns:
            list[dict[str, Any]] | int: The query results as a list of dictionaries,
            or 500 if an error occurs.
        """
        try:
            query = """
            SELECT
                event,
                COUNT(*) AS event_occurrences
            FROM game_plays
            GROUP BY event
            ORDER BY event_occurrences DESC;
            """
            self._cursor.execute(query)

            rows = self._cursor.fetchall()
            rows = cast(list[dict[str, Any]], rows)

            return rows

        except Exception:
            return 500

    def execute_topshootingteams(self) -> list[dict[str, Any]] | int:
        """
        Execute a query to find the teams with the most shots.

        Returns:
            list[dict[str, Any]] | int: The query results as a list of dictionaries,
            or 500 if an error occurs.
        """
        try:
            query = """
            SELECT
                shortName + ' ' + teamName AS team_name,
                SUM(game_teams_stats.shots) AS total_shots
            FROM game_teams_stats
            JOIN team_info ON game_teams_stats.team_id = team_info.team_id
            GROUP BY shortName, teamName
            ORDER BY total_shots DESC;
            """
            self._cursor.execute(query)

            rows = self._cursor.fetchall()
            rows = cast(list[dict[str, Any]], rows)

            return rows

        except Exception:
            return 500

    def execute_playerswithmostassists(self) -> list[dict[str, Any]] | int:
        """
        Execute a query to find the players with the most assists.

        Returns:
            list[dict[str, Any]] | int: The query results as a list of dictionaries,
            or 500 if an error occurs.
        """
        try:
            query = """
            SELECT TOP 10
                player_id,
                season,
                SUM(assists) AS total_assists
            FROM game_skater_stats
            JOIN player_info ON game_skater_stats.player_id = player_info.player_id
            JOIN game ON game_skater_stats.game_id = game.game_id
            GROUP BY player_id, season
            ORDER BY total_assists DESC;
            """
            self._cursor.execute(query)

            rows = self._cursor.fetchall()
            rows = cast(list[dict[str, Any]], rows)

            return rows

        except Exception:
            return 500

    def execute_longestgames(self) -> list[dict[str, Any]] | int:
        """
        Execute a query to find the longest games based on the number of events.

        Returns:
            list[dict[str, Any]] | int: The query results as a list of dictionaries,
            or 500 if an error occurs.
        """
        try:
            query = """
            SELECT TOP 10
                game_id,
                COUNT(*) AS num_events
            FROM game_plays
            GROUP BY game_id
            ORDER BY num_events DESC;
            """
            self._cursor.execute(query)

            rows = self._cursor.fetchall()
            rows = cast(list[dict[str, Any]], rows)

            return rows

        except Exception:
            return 500

    def execute_playerswithlongestavgshift(self) -> list[dict[str, Any]] | int:
        """
        Execute a query to find the players with the longest average shift duration.

        Returns:
            list[dict[str, Any]] | int: The query results as a list of dictionaries,
            or 500 if an error occurs.
        """
        try:
            query = """
            SELECT TOP 20
                pi.firstName + ' ' + pi.lastName AS player_name,
                pi.primaryPosition,
                pi.shootsCatches,
                COUNT(*) AS total_shifts,
                AVG(gs.shift_end - gs.shift_start) AS avg_shift_duration_seconds,
                MAX(gs.shift_end - gs.shift_start) AS longest_shift_seconds,
                SUM(gs.shift_end - gs.shift_start) AS total_ice_time_seconds
            FROM game_shifts gs
            INNER JOIN player_info pi ON gs.player_id = pi.player_id
            GROUP BY
                gs.player_id,
                pi.firstName,
                pi.lastName,
                pi.primaryPosition,
                pi.shootsCatches
            HAVING COUNT(*) >= 100
            ORDER BY avg_shift_duration_seconds DESC;
            """
            self._cursor.execute(query)

            rows = self._cursor.fetchall()
            rows = cast(list[dict[str, Any]], rows)

            return rows

        except Exception:
            return 500

    def execute_topscoringplayers(
        self, penalty_threshold: int, minimum_goals: int, limit_rows: int
    ) -> list[dict[str, Any]] | int:
        """
        Execute a query to find the top scoring players excluding those
        who exceed a penalty threshold.

        Args:
            penalty_threshold (int): The maximum number of penalties a player can have.
            minimum_goals (int): The minimum number of goals a player must have scored.
            limit_rows (int): The maximum number of rows to return.

        Returns:
            list[dict[str, Any]] | int: The query results as a list of dictionaries,
            or 500 if an error occurs.
        """
        try:
            query = """
            WITH penalty_prone_players AS (
                SELECT player_id
                FROM game_penalties
                GROUP BY player_id
                HAVING COUNT(*) > %d
            )
            SELECT TOP %d
                p.player_id,
                p.firstName,
                p.lastName,
                p.primaryPosition,
                COUNT(DISTINCT gg.game_id) AS games_with_goals,
                SUM(CASE WHEN gg.strength = 'EVEN' THEN 1 ELSE 0 END) AS
                even_strength_goals,
                SUM(CASE WHEN gg.strength = 'PPG' THEN 1 ELSE 0 END) AS power_play_goals,
                COUNT(*) AS total_goals
            FROM game_goals gg
            JOIN player_info p ON gg.player_id = p.player_id
            WHERE gg.player_id NOT IN (SELECT player_id FROM penalty_prone_players)
                AND p.primaryPosition IN ('C', 'LW', 'RW', 'D')
            GROUP BY p.player_id, p.firstName, p.lastName, p.primaryPosition
            HAVING COUNT(*) >= %d
            ORDER BY total_goals DESC
            """
            self._cursor.execute(query, (penalty_threshold, limit_rows, minimum_goals))

            rows = self._cursor.fetchall()
            rows = cast(list[dict[str, Any]], rows)

            return rows

        except Exception:
            return 500

    def execute_playerswhoscorebutnotassist(
        self, minimum_goals: int, limit_rows: int
    ) -> list[dict[str, Any]] | int:
        """
        Execute a query to find players who score goals but do not provide assists.

        Args:
            minimum_goals (int): The minimum number of goals a player must have scored.
            limit_rows (int): The maximum number of rows to return.

        Returns:
            list[dict[str, Any]] | int: The query results as a list of dictionaries,
            or 500 if an error occurs.
        """
        try:
            query = """
            WITH goal_scorers AS (
                SELECT DISTINCT player_id
                FROM game_goals
            ),
            assist_providers AS (
                SELECT DISTINCT player_id
                FROM game_plays_players
                WHERE playerType = 'Assist'
            )
            SELECT TOP %d
                p.player_id,
                p.firstName,
                p.lastName,
                p.primaryPosition,
                COUNT(DISTINCT gg.game_id) AS games_played,
                COUNT(*) AS total_goals,
                SUM(CASE WHEN gg.strength = 'EVEN' THEN 1 ELSE 0 END) AS
                even_strength_goals,
                SUM(CASE WHEN gg.strength = 'PPG' THEN 1 ELSE 0 END) AS power_play_goals,
                SUM(CASE WHEN gg.emptyNet = 1 THEN 1 ELSE 0 END) AS empty_net_goals
            FROM game_goals gg
            JOIN player_info p ON gg.player_id = p.player_id
            WHERE gg.player_id IN (SELECT player_id FROM goal_scorers)
                AND gg.player_id NOT IN (SELECT player_id FROM assist_providers)
            GROUP BY p.player_id, p.firstName, p.lastName, p.primaryPosition
            HAVING COUNT(*) >= %d
            ORDER BY total_goals DESC
            """
            self._cursor.execute(query, (limit_rows, minimum_goals))

            rows = self._cursor.fetchall()
            rows = cast(list[dict[str, Any]], rows)

            return rows

        except Exception:
            return 500
