import math
import os
import tempfile

import mtgdb.card
import mtgdb.database

# Helper functions
def create_db_helper() -> mtgdb.database.Database:
    global directory
    directory = tempfile.TemporaryDirectory()
    return mtgdb.database.Database(os.path.join(directory.name, "test.db"))

def create_card_helper() -> mtgdb.card.Card:
    return mtgdb.card.Card("abc", "123", True, "Test", 3.21)

# Database creation
def test_db_creation():
    directory = tempfile.TemporaryDirectory()
    filename = os.path.join(directory.name, "test.db")
    assert False == os.path.exists(filename)
    db = mtgdb.database.Database(filename)
    assert True == os.path.exists(filename)

# Adding
def test_adding_one_new_card():
    db = create_db_helper()
    card = create_card_helper()
    db.add(card, 1)
    found = db.search(card)
    assert found.card == card
    assert found.count == 1
    assert found.prev_price == card.price
    assert found.price_diff == 0

def test_adding_many_new_card():
    db = create_db_helper()
    card = create_card_helper()
    db.add(card, 5)
    found = db.search(card)
    assert found.card == card
    assert found.count == 5
    assert found.prev_price == card.price
    assert found.price_diff == 0

def test_adding_one_old_card():
    db = create_db_helper()
    card = create_card_helper()
    db.add(card, 1)
    db.add(card, 1)
    found = db.search(card)
    assert found.card == card
    assert found.count == 2
    assert found.prev_price == card.price
    assert found.price_diff == 0

def test_adding_many_old_card():
    db = create_db_helper()
    card = create_card_helper()
    db.add(card, 1)
    db.add(card, 5)
    found = db.search(card)
    assert found.card == card
    assert found.count == 6
    assert found.prev_price == card.price
    assert found.price_diff == 0

def test_adding_multiple_different_cards():
    db = create_db_helper()
    card1 = mtgdb.card.Card("abc", "123", True, "Test1", 3.21)
    card2 = mtgdb.card.Card("def", "456", False, "Test2", 6.54)
    card3 = mtgdb.card.Card("ghi", "789", True, "Test3", 9.87)
    db.add(card1, 1)
    db.add(card2, 2)
    db.add(card3, 3)
    found = db.search(card1)
    assert found.card == card1
    assert found.count == 1
    assert found.prev_price == card1.price
    assert found.price_diff == 0
    found = db.search(card2)
    assert found.card == card2
    assert found.count == 2
    assert found.prev_price == card2.price
    assert found.price_diff == 0
    found = db.search(card3)
    assert found.card == card3
    assert found.count == 3
    assert found.prev_price == card3.price
    assert found.price_diff == 0

# Removing
def test_removing_one_under_card_count():
    db = create_db_helper()
    card = create_card_helper()
    db.add(card, 5)
    db.remove(card, 1)
    found = db.search(card)
    assert found.card == card
    assert found.count == 4
    assert found.prev_price == card.price
    assert found.price_diff == 0

def test_removing_many_under_card_count():
    db = create_db_helper()
    card = create_card_helper()
    db.add(card, 5)
    db.remove(card, 2)
    found = db.search(card)
    assert found.card == card
    assert found.count == 3
    assert found.prev_price == card.price
    assert found.price_diff == 0

def test_removing_one_exactly_card_count():
    db = create_db_helper()
    card = create_card_helper()
    db.add(card, 1)
    db.remove(card, 1)
    found = db.search(card)
    assert found == None

def test_removing_many_exactly_card_count():
    db = create_db_helper()
    card = create_card_helper()
    db.add(card, 5)
    db.remove(card, 5)
    found = db.search(card)
    assert found == None

def test_removing_many_over_one_card_count():
    db = create_db_helper()
    card = create_card_helper()
    db.add(card, 1)
    db.remove(card, 5)
    found = db.search(card)
    assert found == None

def test_removing_many_over_card_count():
    db = create_db_helper()
    card = create_card_helper()
    db.add(card, 2)
    db.remove(card, 5)
    found = db.search(card)
    assert found == None

def test_removing_one_nonexistent_card():
    db = create_db_helper()
    card = create_card_helper()
    db.remove(card, 1)
    found = db.search(card)
    assert found == None

def test_removing_many_nonexistent_card():
    db = create_db_helper()
    card = create_card_helper()
    db.remove(card, 5)
    found = db.search(card)
    assert found == None

def test_removing_multiple_different_cards():
    db = create_db_helper()
    card1 = mtgdb.card.Card("abc", "123", True, "Test1", 3.21)
    card2 = mtgdb.card.Card("def", "456", False, "Test2", 6.54)
    card3 = mtgdb.card.Card("ghi", "789", True, "Test3", 9.87)
    db.add(card1, 1)
    db.add(card2, 2)
    db.add(card3, 3)
    db.remove(card1, 2)
    db.remove(card2, 2)
    db.remove(card3, 2)
    found = db.search(card1)
    assert found == None
    found = db.search(card2)
    assert found == None
    found = db.search(card3)
    assert found.card == card3
    assert found.count == 1
    assert found.prev_price == card3.price
    assert found.price_diff == 0

# Updating
def test_updating_lower_price():
    db = create_db_helper()
    card = create_card_helper()
    db.add(card, 1)
    new_card = mtgdb.card.Card(card.set_code, card.collector_number,
                               card.foil, card.name, card.price - 1.23)
    db.update(new_card)
    found = db.search(card)
    assert found.card == new_card
    assert found.count == 1
    assert found.prev_price == card.price
    assert True == math.isclose(found.price_diff, -1.23)

def test_updating_higher_price():
    db = create_db_helper()
    card = create_card_helper()
    db.add(card, 1)
    new_card = mtgdb.card.Card(card.set_code, card.collector_number,
                               card.foil, card.name, card.price + 1.23)
    db.update(new_card)
    found = db.search(card)
    assert found.card == new_card
    assert found.count == 1
    assert found.prev_price == card.price
    assert True == math.isclose(found.price_diff, 1.23)

def test_updating_nonexistent_card():
    db = create_db_helper()
    card = create_card_helper()
    db.update(card)
    found = db.search(card)
    assert found == None

# Searching
def test_searching_card():
    db = create_db_helper()
    card1 = mtgdb.card.Card("abc", "123", True, "Test1", 3.21)
    card2 = mtgdb.card.Card("def", "456", False, "Test2", 6.54)
    card3 = mtgdb.card.Card("ghi", "789", True, "Test3", 9.87)
    db.add(card1, 1)
    db.add(card2, 2)
    db.add(card3, 3)
    found = db.search(card1)
    assert found.card == card1
    assert found.count == 1
    assert found.prev_price == card1.price
    assert found.price_diff == 0
    found = db.search(card2)
    assert found.card == card2
    assert found.count == 2
    assert found.prev_price == card2.price
    assert found.price_diff == 0
    found = db.search(card3)
    assert found.card == card3
    assert found.count == 3
    assert found.prev_price == card3.price
    assert found.price_diff == 0

def test_searching_nonexistent_card():
    db = create_db_helper()
    card = create_card_helper()
    found = db.search(card)
    assert found == None

# CSV
def test_make_csv():
    directory = tempfile.TemporaryDirectory()
    filename = os.path.join(directory.name, "test.csv")
    assert False == os.path.exists(filename)
    db = create_db_helper()
    db.make_csv(filename)
    assert True == os.path.exists(filename)
    assert 0 == os.path.getsize(filename)
    card = create_card_helper()
    db.add(card, 1)
    db.make_csv(filename)
    assert True == os.path.exists(filename)
    assert 0 != os.path.getsize(filename)
