import argparse

from mtgdb.card import Card 
from mtgdb.database import Database
from mtgdb.lookup import lookup

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--foil", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-a", "--add", nargs=3, metavar=("SET", "NUM", "COUNT"))
    group.add_argument("-r", "--remove", nargs=3, metavar=("SET", "NUM", "COUNT"))
    group.add_argument("-u", "--update", nargs=2, metavar=("SET", "NUM"))
    group.add_argument("-s", "--search", nargs=2, metavar=("SET", "NUM"))
    args=parser.parse_args()
    assert 1 == sum(arg != None for arg in (args.add, args.remove, args.update, args.search))
    return args

def add(set_code, collector_number, foil, count):
    card = lookup(set_code, collector_number, foil)
    result = database.add(card, count)
    print(f"Added {count} {card}")
    print(result)

def remove(set_code, collector_number, foil, count):
    card = lookup(set_code, collector_number, foil)
    result = database.remove(card, count)
    print(f"Removed {count} {card}")
    print(result)

def update(set_code, collector_number, foil):
    card = lookup(set_code, collector_number, foil)
    result = database.add(card)
    print(result)

def search(set_code, collector_number, foil):
    card = lookup(set_code, collector_number, foil)
    result = database.search(card)
    print(result)

def main():
    args = parse_args()

    database = database.Database("mtgdb.db")

    if args.add != None:
        add(args.add[0], args.add[1], args.foil, args.add[2])
    elif args.remove != None:
        remove(args.remove[0], args.remove[1], args.foil, args.remove[2])
    elif args.update != None:
        update(args.update[0], args.update[1], args.foil)
    elif args.search != None:
        search(args.update[0], args.update[1], args.foil)
    else:
        # Should never happen. parse_args should require at least one
        print("No operation selected")
        assert any(arg != None for arg in (args.add, args.remove, args.update, args.search))

if __name__ == "__main__":
    main()
