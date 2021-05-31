import csv
from dataclasses import dataclass
import sqlite3
from typing import Optional

import mtgdb.card 

@dataclass
class SearchResult:
    card: mtgdb.card.Card
    count: int

class Database:
    def __init__(self, filename: str) -> None:
        self.con = sqlite3.connect(filename)
        cur = self.con.execute("""SELECT COUNT(*) FROM sqlite_master
                                  WHERE type='table' AND name='cards'""")
        if cur.fetchone()[0] == 0:
            print(f"Creating table 'cards' in database '{filename}'")
        self.con.execute("""CREATE TABLE IF NOT EXISTS cards
                            (set_code TEXT NOT NULL,
                             collector_number TEXT NOT NULL,
                             foil INTEGER NOT NULL,
                             name TEXT NOT NULL,
                             count INTEGER NOT NULL CHECK (count > 0),
                             price REAL NOT NULL CHECK (price > 0),
                             prev_price REAL NOT NULL CHECK (prev_price > 0),
                             price_diff REAL NOT NULL,
                             PRIMARY KEY(set_code,
                                         collector_number,
                                         foil))""")

    def __del__(self) -> None:
        self.con.commit()
        self.con.close()

    def add(self, card: mtgdb.card.Card, count: int) -> None:
        assert card is not None
        assert count > 0
        search = self.search(card)
        if search is not None:
            self.con.execute("""UPDATE cards
                                SET count=count+?,
                                    price=?, prev_price=price,
                                    price_diff=?-price
                                WHERE set_code=?
                                      AND collector_number=?
                                      AND foil=?""", 
                             (count, card.price, card.price,
                              card.set_code, card.collector_number,
                              card.foil))
        elif search is None:
            self.con.execute("INSERT INTO cards VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                             (card.set_code, card.collector_number, card.foil,
                              card.name, count, card.price, card.price, 0))

    def remove(self, card: mtgdb.card.Card, count: int) -> None:
        assert card is not None
        assert count > 0
        search = self.search(card)
        if search is None:
            return
        if count >= search.count:
            self.con.execute("""DELETE FROM cards
                                WHERE set_code=?
                                      AND collector_number=?
                                      AND foil=?""",
                                (card.set_code, card.collector_number,
                                 card.foil))
        elif count < search.count:
             self.con.execute("""UPDATE cards
                                SET count=count-?,
                                    price=?, prev_price=price,
                                    price_diff=?-price
                                WHERE set_code=?
                                      AND collector_number=?
                                      AND foil=?""", 
                             (count, card.price, card.price,
                              card.set_code, card.collector_number,
                              card.foil))

    def update(self, card: mtgdb.card.Card) -> None:
        assert card is not None
        self.con.execute("""Update cards
                            SET price=?, prev_price=price, price_diff=?-price
                            WHERE set_code=?
                                  AND collector_number=?
                                  AND foil=?""",
                         (card.price, card.price,
                          card.set_code, card.collector_number,
                          card.foil))

    def search(self, card: mtgdb.card.Card) -> Optional[SearchResult]:
        assert card is not None
        cur = self.con.execute("""SELECT set_code, collector_number, foil,
                                         name, count, price
                                  FROM cards
                                  WHERE set_code=?
                                        AND collector_number=?
                                        AND foil=?""",
                               (card.set_code, card.collector_number,
                                card.foil))
        result = cur.fetchone()
        if result is None:
            return None
        else:
            return SearchResult(mtgdb.card.Card(result[0], result[1], result[2],
                                                result[3], result[5]),
                                result[4])
    def make_csv(self) -> None:
        with open("mtgdb.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, dialect="excel")
            for row in self.con.execute("SELECT * FROM cards"):
                writer.writerow(row)
