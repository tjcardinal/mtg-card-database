import scrython

class Card:
    def __init__(self, set_code, collector_number, foil, name, price):
        self.set_code = set_code
        self.collector_number = collector_number
        self.foil = foil
        self.name = name
        self.price = price

    def __repr__(self):
        return str(self.__dict__)

def lookup(set_code, collector_number, foil):
   card = scrython.cards.Collector(code=set_code, collector_number=collector_number)
   if foil:
       mode = "usd_foil"
   else:
       mode = "usd"
   return Card(found.set_code(), found.collector_number(), foil, found.name(), found.prices(mode))
