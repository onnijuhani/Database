import sqlite3

conn = sqlite3.connect('../cs_database.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS match_data (
    match_id INTEGER PRIMARY KEY,
    event TEXT,
    team1 TEXT,
    team2 TEXT,
    map TEXT,
    t1Score INTEGER,
    t2Score INTEGER,
    t1FH INTEGER,
    t1SH INTEGER,
    t2FH INTEGER,
    t2SH INTEGER,
    t1Clutch INTEGER,
    t2Clutch INTEGER,
    t1FK INTEGER,
    t2FK INTEGER,
    t1Rating REAL,
    t2Rating REAL,
    type TEXT,
    date DATE,
    mapNumber TEXT,
    winner INTEGER,
    t1Level Integer,
    t2Level Integer
)''')

c.execute('''CREATE TABLE IF NOT EXISTS player_data (
    match_id INTEGER,
    player_name TEXT,
    team_name TEXT,
    kills INTEGER,
    deaths INTEGER,
    kd_ratio REAL,
    adr REAL,
    fk_diff INTEGER,
    rating REAL,
    player_id INTEGER,
    date DATE,
    FOREIGN KEY (match_id) REFERENCES match_data (match_id)
  )''')


c.execute('''CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    current_team TEXT,
    total_maps_played INTEGER,
    last_match_id INTEGER,
    FOREIGN KEY (player_id) REFERENCES player_data (player_id)
  )''')

c.execute('''CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL,
    last_match_id INTEGER,
    FOREIGN KEY (team_name) REFERENCES line_ups (team_name)
  )''')

c.execute('''CREATE TABLE IF NOT EXISTS line_ups (
    team_id INTEGER,
    team_name TEXT,
    player_id INTEGER,
    player_name TEXT,
    start_date DATE,
    end_date DATE,
    games_played INTEGER,
    FOREIGN KEY (team_id) REFERENCES teams (team_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id)
  )''')

c.execute('''CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT,
    event_start_date DATE,
    event_end_date DATE,
    event_type TEXT,
    event_level TEXT,
    event_score INTEGER,
    winner_id INTEGER,
    FOREIGN KEY (winner_id) REFERENCES teams (team_id)
  )''')




