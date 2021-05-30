from mtgdb import lookup

def test_foil():
    card = lookup.lookup("shm", "211", True)
    assert "shm" == card.set_code
    assert "211" == card.collector_number
    assert True == card.foil
    assert "Manamorphose" == card.name
    assert 0 < card.price

def test_non_foil():
    card = lookup.lookup("shm", "211", False)
    assert "shm" == card.set_code
    assert "211" == card.collector_number
    assert False == card.foil
    assert "Manamorphose" == card.name
    assert 0 < card.price

def test_non_integer_set_code():
    card = lookup.lookup("ust", "49d", True)
    assert "ust" == card.set_code
    assert "49d" == card.collector_number
    assert True == card.foil
    assert "Very Cryptic Command" == card.name
    assert 0 < card.price

def test_invalid_set_code():
    card = lookup.lookup("abc", "211", True)
    assert None == card

def test_empty_set_code():
    card = lookup.lookup("", "211", True)
    assert None == card

def test_none_set_code():
    card = lookup.lookup(None, "211", True)
    assert None == card

def test_invalid_collector_number():
    card = lookup.lookup("shm", "999", True)
    assert None == card

def test_empty_collector_number():
    card = lookup.lookup("shm", "", True)
    assert None == card

def test_empty_collector_number():
    card = lookup.lookup("shm", None, True)
    assert None == card
