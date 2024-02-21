import pandas as pd
import sqlite3


def insert_teams(database, df):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    try:
        c.execute('DELETE FROM match_data')
        for _, row in df.iterrows():
            print(_,row)
            c.execute('''
                INSERT INTO match_data (
                    match_id, event, team1, team2, map, t1Score, t2Score, 
                    t1FH, t1SH, t2FH, t2SH, t1Clutch, t2Clutch, t1FK, t2FK,
                    t1Rating, t2Rating, type, date, mapNumber, winner, t1Level, t2Level
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            ''', (
                row['match_id'], row['event'], row['team1'], row['team2'],
                row['map'], row['t1Score'], row['t2Score'],
                row['t1FH'], row['t1SH'], row['t2FH'], row['t2SH'],
                row['t1Clutch'], row['t2Clutch'], row['t1FK'], row['t2FK'],
                row['t1Rating'], row['t2Rating'], row['type'], row['date'],
                row['mapNumber'], row['winner'], row['t1Level'], row['t2Level']
            ))

        conn.commit()
        print("Joukkueet lisätty onnistuneesti")
    except sqlite3.Error as e:
        print("Virhe lisättäessä joukkueita tietokantaan:", e)
    finally:
        conn.close()


def insert_player_data(database, df):

    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute('DELETE FROM player_data')

    for index, row in df.iterrows():
        # Pelaajatietojen lisääminen joukkueesta 1
        for player_num in range(1, 6):  # Joukkue 1:n pelaajat ovat sarakkeissa 23-57
            start_col = 22 + (player_num - 1) * 7
            end_col = start_col + 7
            player_data = row[start_col:end_col]
            kills, deaths = map(int, player_data.iloc[2].split(' - '))
            team_name = row["team1"]
            c.execute('''
                INSERT INTO player_data (
                match_id, player_name, team_name, kills,
                deaths, kd_ratio, adr, fk_diff, rating, player_id, date
                ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['match_id'],
                player_data.iloc[0], team_name, kills, deaths,
                float(player_data.iloc[3]),
                float(player_data.iloc[4]),
                int(player_data.iloc[5]),
                float(player_data.iloc[6]),
                None,
                row["date"]))

        # Pelaajatietojen lisääminen joukkueesta 2
        for player_num in range(1, 6):  # Joukkue 2:n pelaajat ovat sarakkeissa 59-93
            start_col = 58 + (player_num - 1) * 7
            end_col = start_col + 7
            player_data = row[start_col:end_col]
            kills, deaths = map(int, player_data.iloc[2].split(' - '))
            team_name = row["team2"]
            c.execute('''
                INSERT INTO player_data (
                match_id, player_name, team_name, kills,
                deaths, kd_ratio, adr, fk_diff, rating, player_id, date
                ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['match_id'],
                player_data.iloc[0], team_name, kills, deaths,
                float(player_data.iloc[3]),
                float(player_data.iloc[4]),
                int(player_data.iloc[5]),
                float(player_data.iloc[6]),
                None,
                row["date"]))

    # Muutosten tallennus ja yhteyden sulkeminen
    conn.commit()
    conn.close()

    print("Pelaajat lisätty onnistuneesti")


def insert_events(database, df):

    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute('DELETE FROM events')

    # Suodatetaan DataFrame, jotta saadaan vain uniikit turnaukset
    unique_events_df = df[['event', 'type', 'event_level', 'event_score']].drop_duplicates()

    for _, row in unique_events_df.iterrows():
        c.execute('''
            INSERT INTO events (
                event_name,
                event_type,
                event_level,
                event_score
            )
            VALUES (
                ?, ?, ?, ?
            )
        ''', (
            row['event'], row['type'], row['event_level'], row['event_score']
        ))

    conn.commit()
    conn.close()

    print("Turnaukset lisätty onnistuneesti")


if __name__ == "__main__":
    data = pd.read_csv('../Tilastot.csv')
    db_file = '../cs_database.db'
    insert_teams(db_file, data)
    insert_player_data(db_file, data)
    insert_events(db_file, data)
