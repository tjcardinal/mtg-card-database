import scrython

from mtgdb.card import Card

def lookup(set_code, collector_number, foil):
   card = scrython.cards.Collector(code=set_code, collector_number=collector_number)
   if foil:
       mode = "usd_foil"
   else:
       mode = "usd"
   return Card(found.set_code(), found.collector_number(), foil, found.name(), found.prices(mode))
