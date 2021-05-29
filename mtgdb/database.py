import sqlite3

from mtgdb import card

class SearchResult:
    def __init__(self, card, count):
        self.card = card
        self.count = count

    def __repr__(self):
        return str(self.__dict__)

class Database:
    def __init__(self, filename):
        self.con = sqlite3.connect(filename)
        cur = self.con.execute("""SELECT COUNT(*) FROM sqlite_master
                                  WHERE type='table' AND name='cards'""")
        if cur.fetchone()[0] == 0:
            print(f"Creating table 'cards' in database '{filename}'")
        self.con.execute("""CREATE TABLE IF NOT EXISTS cards
                            (scryfall_id TEXT NOT NULL, is_foil INTEGER NOT NULL,
                             name TEXT NOT NULL, set_code TEXT NOT NULL,
                             collector_number TEXT NOT NULL,
                             price REAL, prev_price REAL,
                             price_diff REAL, count INTEGER NOT NULL,
                             PRIMARY KEY(scryfall_id, is_foil))""")

    def __del__(self):
        self.con.commit()
        self.con.close()

    def add(self, card, count):
        pass

    def remove(self, card, count):
        pass

    def update(self, card):
        pass

    def search(self, card):
        pass

