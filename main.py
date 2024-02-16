import sqlite3

conn = sqlite3.connect('my_practice_database.db')
c = conn.cursor()

c.execute('''DROP TABLE team_data''')

c.execute('''CREATE TABLE IF NOT EXISTS team_data (
    id INTEGER PRIMARY KEY,
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
    t1Rating REAL,
    t2Rating REAL,
    type TEXT,
    date DATE,
    mapNumber INTEGER,
    winner TEXT     
)''')


c.execute('''DROP TABLE player_data''')

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
    FOREIGN KEY (match_id) REFERENCES team_data (id)
  )''')

