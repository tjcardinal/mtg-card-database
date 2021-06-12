import time
from typing import Optional

import scrython  # type: ignore

import mtgdb.card


def lookup(
    set_code: str, collector_number: str, foil: bool
) -> Optional[mtgdb.card.Card]:
    time.sleep(0.1)
    try:
        found = scrython.cards.Collector(
            code=set_code, collector_number=collector_number
        )
        if foil:
            mode = "usd_foil"
        else:
            mode = "usd"
        return mtgdb.card.Card(
            found.set_code(),
            found.collector_number(),
            foil,
            found.name(),
            float(found.prices(mode)),
        )
    except Exception as e:
        print(e)
        return None
