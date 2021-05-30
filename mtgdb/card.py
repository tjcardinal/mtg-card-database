from dataclasses import dataclass

@dataclass
class Card:
    set_code: str
    collector_number: str
    foil: bool
    name: str
    price: float
