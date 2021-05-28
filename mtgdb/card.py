class Card:
    def __init__(self, set_code, collector_number, foil, name, price):
        self.set_code = set_code
        self.collector_number = collector_number
        self.foil = foil
        self.name = name
        self.price = price

    def __repr__(self):
        return str(self.__dict__)
