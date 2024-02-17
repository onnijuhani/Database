import sqlite3
import pandas as pd




def insert_players_from_database(db_file):
    # Avaa tietokantayhteys
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    try:
        # Poista kaikki pelaajat players-taulusta
        c.execute("DELETE FROM players")

        # Lisää pelaajat tietokannasta
        c.execute('''
            INSERT INTO players (player_name)
            SELECT DISTINCT player_name FROM player_data
        ''')

        conn.commit()
        print("Pelaajat lisätty onnistuneesti")
    except sqlite3.Error as e:
        print("Virhe lisättäessä pelaajia:", e)

    conn.close()


def add_player_id_to_player_data(db_file):
    # Avaa tietokantayhteys
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute('''UPDATE player_data SET player_id = NULL;''')

    # Haetaan player_data-taulusta pelaajat, joilla ei ole player_id:tä
    c.execute('''
            SELECT DISTINCT player_name, match_id FROM player_data
            WHERE player_id IS NULL
        ''')
    players_without_id = c.fetchall()

    for player, match_id in players_without_id:
        player_name = player

        # Etsitään pelaajan player_id players-taulusta
        c.execute('''
                SELECT player_id FROM players
                WHERE player_name = ?
            ''', (player_name,))
        results = c.fetchall()

        if results:
            if len(results) == 1:
                # Jos pelaajalle löytyy yksi ID, päivitetään se suoraan
                player_id = results[0][0]
                c.execute('''
                        UPDATE player_data
                        SET player_id = ?
                        WHERE player_name = ?
                        AND match_id = ?
                    ''', (player_id, player_name, match_id))
            else:
                print(f"Useita pelaajia samalla nimellä '{player_name}' löydetty pelissä {match_id}:")
                for idx, result in enumerate(results):
                    # Tulostetaan pelaajan nimi ja pelaajan ID player-taulukosta
                    print(f"{idx + 1}. Pelaaja: {player_name} | Pelaajan ID: {result[0]}")

                while True:
                    selected_player_id = input("Valitse käytettävä pelaajan ID (tyhjä peruttaa): ")
                    if not selected_player_id:
                        print("Operaatio peruutettu.")
                        break
                    selected_player_id = int(selected_player_id)
                    if selected_player_id in [result[0] for result in results]:
                        c.execute('''
                                UPDATE player_data
                                SET player_id = ?
                                WHERE player_name = ?
                                AND match_id = ?
                            ''', (selected_player_id, player_name, match_id))
                        print("Pelaajan ID päivitetty onnistuneesti.")
                        break
                    else:
                        print("Virheellinen valinta. Valitse käytettävä pelaajan ID.")
        else:
            print(f"Pelaajalle '{player_name}' ei löytynyt vastaavaa ID:tä players-taulusta pelissä {match_id}.")

    conn.commit()
    conn.close()

    print("Pelaajien ID:t päivitetty onnistuneesti")




def add_new_player(db_file):
    # Avaa tietokantayhteys
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    new_player_name = input("Syötä uuden pelaajan nimi: ")

    try:
        # Lisää uusi pelaaja player-tauluun
        c.execute("INSERT INTO players (player_name) VALUES (?)", (new_player_name,))
        conn.commit()
        print("Uusi pelaaja lisätty onnistuneesti.")
    except sqlite3.Error as e:
        print("Virhe lisättäessä uutta pelaajaa:", e)

    conn.close()


def update_player_team(db_file):
    # Avaa tietokantayhteys
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute('''UPDATE players SET Team = NULL;''')

    # Haetaan pelaajat, joiden joukkueita ei ole päivitetty
    c.execute('''
        SELECT DISTINCT player_name
        FROM players
        WHERE Team IS NULL
    ''')
    players_without_team = c.fetchall()

    for player_name, in players_without_team:
        # Etsitään pelaajan viimeisin joukkue player_data-taulukosta päiväyksen perusteella
        c.execute('''
            SELECT team_name
            FROM player_data
            WHERE player_name = ?
            ORDER BY date DESC
            LIMIT 1
        ''', (player_name,))
        team_result = c.fetchone()
        if team_result:
            team_name = team_result[0]
            c.execute('''
                UPDATE players
                SET Team = ?
                WHERE player_name = ?
            ''', (team_name, player_name))

    conn.commit()
    conn.close()

    print("Pelaajien joukkueet päivitetty onnistuneesti")


if __name__ == "__main__":
    db_file = 'my_practice_database.db'  # Tietokantatiedoston nimi
    update_player_team(db_file)
