import time

import scrython

from mtgdb import card

def lookup(set_code, collector_number, foil):

    time.sleep(0.1)
    found = scrython.cards.Collector(code=set_code,
                                     collector_number=collector_number)
    if foil:
        mode = "usd_foil"
    else:
        mode = "usd"
    return card.Card(found.set_code(), found.collector_number(), foil,
                     found.name(), found.prices(mode))
