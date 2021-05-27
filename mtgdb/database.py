import sqlite3

from card_lookup import Card

class SearchResult:
    def __init__(card, count):
        self.card = card
        self.count = count

    def __repr__(self):
        return str(self.__dict__)

class Database:
    def __init__(filename):
        pass

    def __del__():
        pass

    def add(card, count):
        pass

    def remove(card, count):
        pass

    def update(card):
        pass

    def search(card):
        pass

