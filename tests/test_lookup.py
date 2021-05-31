import mtgdb.lookup

def test_foil():
    card = mtgdb.lookup.lookup("shm", "211", True)
    assert "shm" == card.set_code
    assert "211" == card.collector_number
    assert True == card.foil
    assert "Manamorphose" == card.name
    assert 0 < card.price

def test_non_foil():
    card = mtgdb.lookup.lookup("shm", "211", False)
    assert "shm" == card.set_code
    assert "211" == card.collector_number
    assert False == card.foil
    assert "Manamorphose" == card.name
    assert 0 < card.price

def test_non_three_letter_set_code():
    card = mtgdb.lookup.lookup("pwp09", "24", True)
    assert "pwp09" == card.set_code
    assert "24" == card.collector_number
    assert True == card.foil
    assert "Path to Exile" == card.name
    assert 0 < card.price

def test_non_integer_collector_number():
    card = mtgdb.lookup.lookup("ust", "49d", True)
    assert "ust" == card.set_code
    assert "49d" == card.collector_number
    assert True == card.foil
    assert "Very Cryptic Command" == card.name
    assert 0 < card.price

def test_invalid_set_code():
    card = mtgdb.lookup.lookup("abc", "211", True)
    assert None == card

def test_empty_set_code():
    card = mtgdb.lookup.lookup("", "211", True)
    assert None == card

def test_none_set_code():
    card = mtgdb.lookup.lookup(None, "211", True)
    assert None == card

def test_invalid_collector_number():
    card = mtgdb.lookup.lookup("shm", "999", True)
    assert None == card

def test_empty_collector_number():
    card = mtgdb.lookup.lookup("shm", "", True)
    assert None == card

def test_none_collector_number():
    card = mtgdb.lookup.lookup("shm", None, True)
    assert None == card
