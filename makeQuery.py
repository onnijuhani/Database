import sqlite3


class Query:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def get_unique_tournaments(self):
        try:
            self.cursor.execute("SELECT DISTINCT event FROM team_data")
            tournaments = self.cursor.fetchall()
            return [event[0] for event in tournaments]
        except sqlite3.Error as e:
            print("Virhe tietokantakyselyssä:", e)
            return None

    def close_connection(self):
        self.conn.close()


# Käyttöesimerkki
if __name__ == "__main__":
    db_file = 'my_practice_database.db'  # Vaihda tietokantatiedoston nimi tarvittaessa
    query = Query(db_file)
    unique_tournaments = query.get_unique_tournaments()
    if unique_tournaments:
        print("Uniikit turnaukset:")
        for tournament in unique_tournaments:
            print(tournament)
    query.close_connection()