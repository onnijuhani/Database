import pandas as pd
import sqlite3

df = pd.read_csv('tilastot.csv')

conn = sqlite3.connect('my_practice_database.db')
c = conn.cursor()

c.execute('DELETE FROM team_data')

for _, row in df.iterrows():
    c.execute('''
        INSERT INTO team_data (
            id, event, team1, team2, map, t1Score, t2Score, 
            t1FH, t1SH, t2FH, t2SH, t1Clutch, t2Clutch, t1Rating, 
            t2Rating, type, date, mapNumber, winner
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    ''', (
        row['Match ID'], row['Turnaus'], row['Joukkue1'], row['Joukkue2'],
        row['Kartta'], row['T1 Score'], row['T2 Score'],
        row['T1 FH'], row['T1 SH'], row['T2 FH'], row['T2 SH'],
        row['T1 Clutches'], row['T2 Clutches'], row['T1 Rating'],
        row['T2 Rating'], row['Tyyppi'], row['Päiväys'], row['MapNro'],
        row['Voittaja']
    ))


conn.commit()
conn.close()

print("Joukkueet lisätty onnistuneesti")