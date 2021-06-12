import argparse

import mtgdb.card
import mtgdb.database
import mtgdb.lookup


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="mtgdb")
    parser.add_argument("--foil", "-f", action="store_true")
    parser.add_argument("--csv", "-c", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--add", "-a", nargs=3, metavar=("SET", "NUM", "COUNT"))
    group.add_argument("--remove", "-r", nargs=3, metavar=("SET", "NUM", "COUNT"))
    group.add_argument("--update", "-u", nargs=2, metavar=("SET", "NUM"))
    group.add_argument("--search", "-s", nargs=2, metavar=("SET", "NUM"))
    group.add_argument("--update-all", action="store_const", const=True)
    args = parser.parse_args()

    if (args.add is not None and int(args.add[2]) <= 0) or (
        args.remove is not None and int(args.remove[2]) <= 0
    ):
        parser.error("COUNT must be >0")

    assert 1 == sum(
        arg is not None
        for arg in (args.add, args.remove, args.update, args.search, args.update_all)
    )

    return args


def add(
    db: mtgdb.database.Database,
    set_code: str,
    collector_number: str,
    foil: bool,
    count: int,
) -> None:
    card = mtgdb.lookup.lookup(set_code, collector_number, foil)
    if card is not None:
        db.add(card, count)
        print(f"Added {count} {card}")
    else:
        print("Lookup failed")


def remove(
    db: mtgdb.database.Database,
    set_code: str,
    collector_number: str,
    foil: bool,
    count: int,
) -> None:
    card = mtgdb.lookup.lookup(set_code, collector_number, foil)
    if card is not None:
        db.remove(card, count)
        print(f"Removed {count} {card}")
    else:
        print("Lookup failed")


def update(
    db: mtgdb.database.Database, set_code: str, collector_number: str, foil: bool
) -> None:
    card = mtgdb.lookup.lookup(set_code, collector_number, foil)
    if card is not None:
        db.update(card)
        print(f"updated {card}")
    else:
        print("Lookup failed")


def search(
    db: mtgdb.database.Database, set_code: str, collector_number: str, foil: bool
) -> None:
    card = mtgdb.lookup.lookup(set_code, collector_number, foil)
    if card is not None:
        result = db.search(card)
        print(result)
    else:
        print("Lookup failed")


def update_all(db: mtgdb.database.Database) -> None:
    records = db.get_all()
    for record in records:
        card = mtgdb.lookup.lookup(
            record.card.set_code, record.card.collector_number, record.card.foil
        )
        if card is not None:
            db.update(card)
        else:
            print("Lookup failed for {record.card}")


def main() -> None:
    args = parse_args()

    db = mtgdb.database.Database("mtgdb.db")

    if args.add is not None:
        add(db, args.add[0], args.add[1], args.foil, int(args.add[2]))
    elif args.remove is not None:
        remove(db, args.remove[0], args.remove[1], args.foil, int(args.remove[2]))
    elif args.update is not None:
        update(db, args.update[0], args.update[1], args.foil)
    elif args.search is not None:
        search(db, args.search[0], args.search[1], args.foil)
    elif args.update_all is not None:
        update_all(db)
    else:
        # Should never happen. parse_args should require at least one
        assert any(
            arg is not None for arg in (args.add, args.remove, args.update, args.search)
        )

    if args.csv is not None:
        db.make_csv("mtgdb.csv")
