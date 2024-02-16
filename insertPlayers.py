import pandas as pd
import sqlite3

df = pd.read_csv('tilastot.csv')
conn = sqlite3.connect('my_practice_database.db')
c = conn.cursor()

c.execute('DELETE FROM player_data')

for index, row in df.iterrows():
    # Pelaajatietojen lisääminen joukkueesta 1
    for player_num in range(1, 6):  # Joukkue 1:n pelaajat ovat sarakkeissa 23-57
        start_col = 22 + (player_num - 1) * 7
        end_col = start_col + 7
        player_data = row[start_col:end_col]
        kills, deaths = map(int, player_data.iloc[2].split(' - '))
        team_name = row["Joukkue1"]
        c.execute('''
            INSERT INTO player_data (match_id, player_name, team_name, kills, deaths, kd_ratio, adr, fk_diff, rating) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row['Match ID'], player_data.iloc[0], team_name, kills, deaths, float(player_data.iloc[3]), float(player_data.iloc[4]),
              int(player_data.iloc[5]), float(player_data.iloc[6])))

    # Pelaajatietojen lisääminen joukkueesta 2
    for player_num in range(1, 6):  # Joukkue 2:n pelaajat ovat sarakkeissa 59-93
        start_col = 58 + (player_num - 1) * 7
        end_col = start_col + 7
        player_data = row[start_col:end_col]
        kills, deaths = map(int, player_data.iloc[2].split(' - '))
        team_name = row["Joukkue2"]
        c.execute('''
            INSERT INTO player_data (match_id, player_name, team_name, kills, deaths, kd_ratio, adr, fk_diff, rating) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row['Match ID'], player_data.iloc[0], team_name, kills, deaths, float(player_data.iloc[3]), float(player_data.iloc[4]),
              int(player_data.iloc[5]), float(player_data.iloc[6])))

# Muutosten tallennus ja yhteyden sulkeminen
conn.commit()
conn.close()

print("Pelaajat lisätty onnistuneesti")

